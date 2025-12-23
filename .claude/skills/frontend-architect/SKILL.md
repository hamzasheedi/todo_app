---
name: frontend-architect
description: Design and implement Next.js 16+ frontend architecture with App Router, TypeScript, and Tailwind CSS for the multi-user todo application following modern best practices
---

# Frontend Architect Skill

## Purpose

This skill should be used when designing and implementing Next.js 16+ frontend architecture with App Router, TypeScript, and Tailwind CSS for the Phase II Todo Full-Stack Web Application. The skill focuses on creating performant, accessible, and maintainable frontend applications following modern best practices.

## When to Use This Skill

Use this skill when:
- Setting up new Next.js 16+ projects with App Router
- Implementing responsive UI components with Tailwind CSS
- Creating server and client components with proper data fetching strategies
- Implementing TypeScript interfaces and type safety
- Optimizing frontend performance and Core Web Vitals
- Ensuring WCAG 2.1 AA compliance and accessibility

## How to Use This Skill

### Next.js App Router Architecture
1. Organize pages using the App Router convention with proper folder structure
2. Implement server components for data fetching and client components for interactivity
3. Use proper metadata files for SEO and social sharing
4. Implement proper error boundaries and loading states
5. Use route groups and parallel routes when appropriate

### Component Design Process
1. Create reusable components with proper TypeScript interfaces
2. Implement responsive design using Tailwind CSS utility classes
3. Ensure mobile-first approach with breakpoints at 768px and 1024px
4. Implement accessibility features following WCAG 2.1 AA guidelines
5. Create component documentation with usage examples

### Performance Optimization
1. Implement code splitting and dynamic imports
2. Optimize images with Next.js Image component
3. Use lazy loading for non-critical components
4. Implement proper caching strategies
5. Optimize bundle size and reduce unused CSS

## Available Resources

### Component Templates
- Use templates in `/frontend/components/templates/` for creating new components
- Follow established patterns for consistency
- Include proper TypeScript interfaces for props
- Implement proper error boundaries

### Page Templates
- Use `/frontend/app/templates/` for creating new page structures
- Follow App Router conventions and best practices
- Include proper metadata and SEO considerations
- Implement loading and error states

### Styling Guidelines
- Follow `/assets/guidelines/responsive_guidelines.md` for responsive design
- Apply `/assets/guidelines/accessibility_checklist.md` for accessibility compliance
- Use `/assets/guidelines/tailwind_guidelines.md` for consistent styling
- Implement proper design tokens and theming

### API Integration
- Reference `/frontend/lib/api-client.ts` for API client implementation
- Use proper error handling and loading states
- Implement proper authentication token management
- Follow consistent API interaction patterns

## Output Standards

When designing frontend implementations:
1. Ensure all components are responsive across mobile, tablet, and desktop
2. Include proper alt text, ARIA attributes, and semantic HTML for accessibility
3. Use consistent color schemes and typography based on Tailwind CSS
4. Create reusable components that follow Next.js best practices
5. Implement proper TypeScript interfaces and type safety
6. Optimize for Core Web Vitals and performance metrics
7. Document any custom design patterns in the component comments