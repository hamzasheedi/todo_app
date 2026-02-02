---
name: ui_ux_designer
description: Design responsive, intuitive frontend interfaces and UX flows for the Phase II Todo Full-Stack Web Application using Next.js and Tailwind CSS.
---

# UI/UX Designer Skill

## Purpose

This skill should be used when designing responsive, intuitive frontend interfaces and UX flows for the Phase II Todo Full-Stack Web Application. The skill focuses on creating user-centered designs using Next.js and Tailwind CSS with accessibility compliance.

## When to Use This Skill

Use this skill when:
- Designing new frontend pages or components for the todo application
- Creating user interface layouts that follow responsive design principles
- Implementing accessibility features (WCAG 2.1 AA compliance)
- Designing user flows for authentication, task management, and sorting features
- Creating component templates for reuse across the application

## How to Use This Skill

### Component Design Process
1. Analyze the user requirements from the specification
2. Design responsive components using Tailwind CSS utility classes
3. Ensure mobile-first approach with breakpoints at 768px and 1024px
4. Implement accessibility features following WCAG 2.1 AA guidelines
5. Create reusable component templates in the templates directory

### Page Layout Design
1. Design Next.js App Router pages with proper layout structure
2. Implement responsive navigation and user interface elements
3. Create consistent design patterns across all pages
4. Ensure proper integration with authentication state management

### User Flow Design
1. Map out user journeys for core functionality (authentication, task CRUD, sorting)
2. Design intuitive navigation between different application states
3. Create error handling UI that provides clear feedback to users
4. Design loading and empty states for all interactive components

## Available Resources

### Component Templates
- Use templates in `/frontend/components/templates/` for creating new components
- Follow established patterns for consistency
- Include proper TypeScript interfaces for props

### UI Flow Diagrams
- Reference `/assets/diagrams/ui_flows.drawio` for user journey mapping
- Update diagrams when creating new user flows
- Ensure all user paths are documented and accessible

### Design Guidelines
- Follow `/assets/guidelines/responsive_guidelines.md` for responsive design
- Apply `/assets/guidelines/accessibility_checklist.md` for accessibility compliance
- Use `/assets/guidelines/tailwind_guidelines.md` for consistent styling

### Next.js Templates
- Use `/frontend/app/templates/` for creating new page structures
- Follow App Router conventions and best practices
- Include proper metadata and SEO considerations

## Output Standards

When designing UI/UX elements:
1. Ensure all components are responsive across mobile, tablet, and desktop
2. Include proper alt text and ARIA attributes for accessibility
3. Use consistent color schemes and typography based on Tailwind CSS
4. Create reusable components that follow Next.js best practices
5. Document any custom design patterns in the component comments