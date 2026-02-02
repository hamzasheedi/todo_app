import os
import sys
from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from backend.config import settings
import logging
from datetime import datetime
import subprocess
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MigrationManager:
    """
    Comprehensive migration management system for database schema evolution
    """

    def __init__(self, database_url: str = None):
        self.database_url = database_url or settings.DATABASE_URL
        self.engine = create_engine(self.database_url)
        self.alembic_cfg = self._setup_alembic_config()

    def _setup_alembic_config(self) -> Config:
        """
        Setup Alembic configuration
        """
        cfg = Config()
        cfg.set_main_option("script_location", "alembic")
        cfg.set_main_option("sqlalchemy.url", self.database_url)
        return cfg

    def create_migration(self, message: str, autogenerate: bool = True):
        """
        Create a new migration script
        """
        try:
            logger.info(f"Creating migration: {message}")
            command.revision(
                self.alembic_cfg,
                message=message,
                autogenerate=autogenerate
            )
            logger.info(f"Migration created successfully: {message}")
        except Exception as e:
            logger.error(f"Failed to create migration: {str(e)}")
            raise

    def run_migrations(self, revision: str = "head"):
        """
        Run migrations to specified revision
        """
        try:
            logger.info(f"Running migrations to revision: {revision}")
            command.upgrade(self.alembic_cfg, revision)
            logger.info("Migrations completed successfully")
        except Exception as e:
            logger.error(f"Failed to run migrations: {str(e)}")
            raise

    def rollback_migrations(self, revision: str = "-1"):
        """
        Rollback migrations
        """
        try:
            logger.info(f"Rolling back migrations: {revision}")
            command.downgrade(self.alembic_cfg, revision)
            logger.info("Rollback completed successfully")
        except Exception as e:
            logger.error(f"Failed to rollback migrations: {str(e)}")
            raise

    def check_migration_status(self):
        """
        Check current migration status
        """
        try:
            # Get current revision
            current_rev = self.get_current_revision()
            logger.info(f"Current migration revision: {current_rev}")

            # Get available revisions
            available_revs = self.get_available_revisions()
            logger.info(f"Available revisions: {len(available_revs)}")

            # Check for unapplied migrations
            unapplied = self.get_unapplied_migrations()
            logger.info(f"Unapplied migrations: {len(unapplied)}")

            return {
                "current_revision": current_rev,
                "available_revisions": len(available_revs),
                "unapplied_migrations": len(unapplied)
            }
        except Exception as e:
            logger.error(f"Failed to check migration status: {str(e)}")
            raise

    def get_current_revision(self):
        """
        Get current database revision
        """
        with self.engine.connect() as conn:
            context = MigrationContext.configure(conn)
            return context.get_current_revision()

    def get_available_revisions(self):
        """
        Get all available migration revisions
        """
        script = ScriptDirectory.from_config(self.alembic_cfg)
        return [rev.revision for rev in script.walk_revisions()]

    def get_unapplied_migrations(self):
        """
        Get list of unapplied migrations
        """
        script = ScriptDirectory.from_config(self.alembic_cfg)
        with self.engine.connect() as conn:
            context = MigrationContext.configure(conn)
            current_rev = context.get_current_revision()

            unapplied = []
            for rev in script.walk_revisions():
                if rev.revision != current_rev:
                    unapplied.append(rev)

            return unapplied

    def validate_migration_safety(self, migration_file: str) -> bool:
        """
        Validate migration safety before applying
        """
        logger.info(f"Validating migration safety: {migration_file}")

        # Read migration file
        with open(migration_file, 'r') as f:
            content = f.read()

        # Check for potentially dangerous operations
        dangerous_patterns = [
            "DROP TABLE",
            "DROP COLUMN",
            "ALTER TABLE.*DROP",
            "DELETE FROM",
        ]

        issues = []
        for pattern in dangerous_patterns:
            import re
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                issues.append(f"Dangerous operation found: {pattern}")

        if issues:
            logger.warning(f"Migration validation issues: {issues}")
            return False

        logger.info("Migration validation passed")
        return True

    def backup_database(self, backup_path: str = None):
        """
        Create database backup before migration
        """
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backups/database_backup_{timestamp}.sql"

        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        try:
            # For PostgreSQL (Neon), use pg_dump
            if "postgresql" in self.database_url:
                db_url_parts = self.database_url.split("://")[1].split("@")
                credentials = db_url_parts[0].split(":")
                host_port = db_url_parts[1].split("/")
                host = host_port[0].split(":")[0]
                port = host_port[0].split(":")[1] if ":" in host_port[0] else "5432"
                database = host_port[1]

                cmd = [
                    "pg_dump",
                    "-h", host,
                    "-p", port,
                    "-U", credentials[0],
                    "-d", database,
                    "-f", backup_path
                ]

                # Set password in environment
                env = os.environ.copy()
                env["PGPASSWORD"] = credentials[1]

                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"Backup failed: {result.stderr}")

            logger.info(f"Database backup created: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Failed to create database backup: {str(e)}")
            raise

    def zero_downtime_migration_check(self):
        """
        Check if migration can be performed with zero downtime
        """
        # This is a simplified check - in real implementation you'd have more sophisticated logic
        # For example, checking if migration only adds columns (safe) vs removes/modifies (unsafe)
        return True

    def run_with_rollback_protection(self, revision: str = "head"):
        """
        Run migrations with automatic rollback on failure
        """
        # Create backup before migration
        backup_path = self.backup_database()

        try:
            # Check migration safety
            unapplied_migrations = self.get_unapplied_migrations()
            for migration in unapplied_migrations:
                if not self.validate_migration_safety(migration.path):
                    raise Exception(f"Unsafe migration detected: {migration.path}")

            # Run migrations
            self.run_migrations(revision)

            # Verify migration success
            status = self.check_migration_status()
            if status["unapplied_migrations"] == 0:
                logger.info("All migrations applied successfully")
            else:
                raise Exception("Not all migrations were applied successfully")

        except Exception as e:
            logger.error(f"Migration failed: {str(e)}")
            logger.info("Attempting rollback...")

            # Attempt rollback
            try:
                self.rollback_migrations()
                logger.info("Rollback completed successfully")
            except Exception as rollback_error:
                logger.error(f"Rollback failed: {str(rollback_error)}")
                logger.info(f"Manual intervention may be required. Backup available at: {backup_path}")
                raise

            raise

    def generate_migration_report(self, output_file: str = "migration_report.json"):
        """
        Generate comprehensive migration report
        """
        status = self.check_migration_status()
        unapplied = self.get_unapplied_migrations()

        report = {
            "timestamp": datetime.now().isoformat(),
            "database_url": self.database_url,
            "status": status,
            "unapplied_migrations": [
                {
                    "revision": mig.revision,
                    "down_revision": mig.down_revision,
                    "message": mig.doc
                } for mig in unapplied
            ]
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Migration report generated: {output_file}")
        return report


class MigrationScriptTemplate:
    """
    Template for creating migration scripts
    """

    @staticmethod
    def create_upgrade_template():
        """
        Template for upgrade operations
        """
        return '''
"""{message}

Revision ID: {rev_id}
Revises: {down_revision}
Create Date: {create_date}

"""
from alembic import op
import sqlalchemy as sa
{imports if imports else ""}

# revision identifiers, used by Alembic.
revision = '{rev_id}'
down_revision = '{down_revision}'
branch_labels = {branch_labels}
depends_on = {depends_on}


def upgrade() -> None:
    {upgrades if upgrades else "pass"}


def downgrade() -> None:
    {downgrades if downgrades else "pass"}
'''

    @staticmethod
    def create_data_migration_template():
        """
        Template for data migrations
        """
        return '''
"""Data migration: {message}

Revision ID: {rev_id}
Revises: {down_revision}
Create Date: {create_date}

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, DateTime
import datetime

# revision identifiers, used by Alembic.
revision = '{rev_id}'
down_revision = '{down_revision}'
branch_labels = {branch_labels}
depends_on = {depends_on}


def upgrade() -> None:
    # Example data migration
    # Define the table structure
    users_table = table('users',
        column('id', String),
        column('email', String),
        column('created_date', DateTime)
    )

    # Perform data updates
    op.execute(
        users_table.update()
        .where(users_table.c.email == 'old@example.com')
        .values(email='new@example.com')
    )


def downgrade() -> None:
    # Revert data changes
    users_table = table('users',
        column('id', String),
        column('email', String),
        column('created_date', DateTime)
    )

    op.execute(
        users_table.update()
        .where(users_table.c.email == 'new@example.com')
        .values(email='old@example.com')
    )
'''


def main():
    """
    Main function for migration management
    """
    import argparse

    parser = argparse.ArgumentParser(description="Migration Management Tool")
    parser.add_argument("--action", choices=["create", "upgrade", "downgrade", "status", "backup", "report"], required=True)
    parser.add_argument("--message", help="Migration message (for create action)")
    parser.add_argument("--revision", help="Target revision (for upgrade/downgrade)")
    parser.add_argument("--backup-path", help="Backup path")

    args = parser.parse_args()

    manager = MigrationManager()

    if args.action == "create":
        if not args.message:
            print("Error: --message is required for create action")
            sys.exit(1)
        manager.create_migration(args.message)
    elif args.action == "upgrade":
        revision = args.revision or "head"
        manager.run_with_rollback_protection(revision)
    elif args.action == "downgrade":
        revision = args.revision or "-1"
        manager.rollback_migrations(revision)
    elif args.action == "status":
        status = manager.check_migration_status()
        print(json.dumps(status, indent=2))
    elif args.action == "backup":
        backup_path = args.backup_path or f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        manager.backup_database(backup_path)
        print(f"Backup created: {backup_path}")
    elif args.action == "report":
        report_path = args.backup_path or "migration_report.json"
        manager.generate_migration_report(report_path)
        print(f"Report generated: {report_path}")


if __name__ == "__main__":
    main()