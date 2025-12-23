try:
    from . import auth, tasks
except ImportError:
    try:
        # Direct import for when module is run directly
        import auth
        import tasks
    except ImportError:
        # Import with full path for test environments
        from . import auth
        from . import tasks

__all__ = ['auth', 'tasks']
