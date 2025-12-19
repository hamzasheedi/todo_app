---
name: responsive-design-specialist
description: Implement advanced mobile-first responsive design with WCAG 2.1 AA compliance, progressive enhancement, and cross-device optimization
---

# Responsive Design Specialist Skill

## Purpose

This skill should be used when implementing advanced mobile-first responsive design with WCAG 2.1 AA compliance, progressive enhancement, and cross-device optimization for the Phase II Todo Full-Stack Web Application. The skill focuses on creating accessible, performant, and user-friendly interfaces across all devices and screen sizes.

## When to Use This Skill

Use this skill when:
- Designing responsive UI components and layouts
- Implementing mobile-first design approaches
- Ensuring WCAG 2.1 AA accessibility compliance
- Optimizing for Core Web Vitals and performance
- Creating cross-browser compatible interfaces
- Implementing progressive enhancement strategies

## How to Use This Skill

### Mobile-First Design Strategy
1. Start design with mobile viewport and constraints
2. Implement progressive enhancement for larger screens
3. Use flexible grids and relative units (rem, em, %)
4. Create touch-friendly interface elements
5. Optimize for thumb-friendly touch targets (44px minimum)
6. Implement proper viewport configurations
7. Test on actual mobile devices and emulators

### Responsive Breakpoints
1. Implement primary breakpoint at 768px (tablet)
2. Add secondary breakpoint at 1024px (desktop)
3. Create additional breakpoints as needed for content
4. Use fluid typography with clamp() where appropriate
5. Implement responsive image strategies
6. Optimize navigation for different screen sizes
7. Test responsiveness across all breakpoints

### Accessibility Implementation
1. Implement WCAG 2.1 AA compliance standards
2. Add proper semantic HTML structure
3. Include ARIA attributes where necessary
4. Ensure proper color contrast ratios (4.5:1 minimum)
5. Implement keyboard navigation support
6. Add screen reader compatibility
7. Test with accessibility tools and real users

### Performance Optimization
1. Optimize images with proper formats and sizes
2. Implement lazy loading for off-screen content
3. Use efficient CSS and minimize render-blocking resources
4. Optimize font loading strategies
5. Implement proper caching and compression
6. Minimize JavaScript bundle sizes
7. Monitor Core Web Vitals metrics

### Cross-Browser Compatibility
1. Test across major browsers (Chrome, Firefox, Safari, Edge)
2. Implement proper vendor prefixes where needed
3. Use feature detection instead of browser detection
4. Implement graceful degradation for unsupported features
5. Test CSS Grid and Flexbox compatibility
6. Validate form input across browsers
7. Ensure consistent behavior across platforms

### Progressive Enhancement
1. Start with basic HTML functionality
2. Add CSS for visual enhancements
3. Implement JavaScript for advanced interactions
4. Ensure core functionality works without JavaScript
5. Add performance enhancements progressively
6. Implement service workers for offline capability
7. Create fallbacks for modern features

## Available Resources

### Design Guidelines
- Use `/assets/guidelines/responsive_guidelines.md` for responsive design
- Reference `/assets/guidelines/accessibility_checklist.md` for accessibility compliance
- Follow `/assets/guidelines/tailwind_guidelines.md` for consistent styling
- Implement proper design system patterns

### Component Templates
- Use `/frontend/components/templates/` for responsive components
- Follow established patterns for consistency
- Include proper TypeScript interfaces for props
- Implement proper accessibility attributes

### Design System
- Reference `/assets/design-system/` for design tokens and components
- Follow established patterns for consistency
- Include proper theming and customization options
- Implement proper documentation and examples

### Tailwind Configuration
- Use `/frontend/styles/` for Tailwind CSS configuration
- Follow established patterns for consistency
- Include proper customization and extensions
- Implement proper optimization strategies

## Output Standards

When implementing responsive design:
1. Ensure mobile-first approach with progressive enhancement
2. Include comprehensive accessibility compliance (WCAG 2.1 AA)
3. Implement proper responsive breakpoints and layouts
4. Optimize for Core Web Vitals and performance metrics
5. Document all design patterns with proper examples
6. Implement proper cross-browser compatibility
7. Optimize for touch interfaces and mobile devices
8. Follow accessibility and responsive design best practices
9. Test all designs across multiple devices and browsers
10. Maintain consistent design patterns across the application