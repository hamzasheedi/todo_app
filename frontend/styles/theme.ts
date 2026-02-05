// Global Theme Tokens
export const themeTokens = {
  colors: {
    // Dark theme base
    background: {
      primary: '#0B0F1A',   // Deep space blue
      secondary: '#0E1424', // Darker blue
      tertiary: '#090C16',  // Darkest blue
      card: '#11162A',      // Card backgrounds
      surface: '#1A1F33',   // Surfaces
    },
    
    // Text colors
    text: {
      primary: '#F5F7FA',   // Light gray
      secondary: '#AAB0C0', // Muted gray
      accent: '#00F5FF',    // Cyan accent
      positive: '#39FF14',  // Bright green
      negative: '#FF1493',  // Pink
      disabled: '#5A6275',  // Disabled state
    },
    
    // Brand accents
    brand: {
      primary: '#00F5FF',   // Cyan
      secondary: '#B026FF', // Purple
      gradient: 'linear-gradient(135deg, #00F5FF 0%, #B026FF 100%)',
    },
    
    // Status colors
    status: {
      success: '#39FF14',
      warning: '#FFD700',
      error: '#FF1493',
      info: '#00F5FF',
    },
  },
  
  typography: {
    fontFamily: {
      sans: 'Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif',
      mono: 'SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace',
    },
    fontSize: {
      xs: '0.75rem',       // 12px
      sm: '0.875rem',      // 14px
      base: '1rem',        // 16px
      lg: '1.125rem',      // 18px
      xl: '1.25rem',       // 20px
      '2xl': '1.5rem',     // 24px
      '3xl': '1.875rem',   // 30px
      '4xl': '2.25rem',    // 36px
      '5xl': '3rem',       // 48px
    },
    fontWeight: {
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
    },
  },
  
  spacing: {
    xs: '0.25rem',    // 4px
    sm: '0.5rem',     // 8px
    md: '1rem',       // 16px
    lg: '1.5rem',     // 24px
    xl: '2rem',       // 32px
    '2xl': '3rem',    // 48px
    '3xl': '4rem',    // 64px
  },
  
  borderRadius: {
    sm: '0.25rem',    // 4px
    md: '0.5rem',     // 8px
    lg: '0.75rem',    // 12px
    xl: '1rem',       // 16px
    '2xl': '1.5rem',  // 24px
    '3xl': '2rem',    // 32px
    full: '9999px',   // Full
  },
  
  boxShadow: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    none: 'none',
  },
  
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
  },
  
  animation: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
    },
    easing: {
      ease: 'ease',
      easeIn: 'ease-in',
      easeOut: 'ease-out',
      easeInOut: 'ease-in-out',
      linear: 'linear',
    },
  },
};

// Export theme as CSS variables for use in Tailwind
export const themeCSSVariables = `
  :root {
    --color-bg-primary: ${themeTokens.colors.background.primary};
    --color-bg-secondary: ${themeTokens.colors.background.secondary};
    --color-bg-tertiary: ${themeTokens.colors.background.tertiary};
    --color-bg-card: ${themeTokens.colors.background.card};
    --color-bg-surface: ${themeTokens.colors.background.surface};
    
    --color-text-primary: ${themeTokens.colors.text.primary};
    --color-text-secondary: ${themeTokens.colors.text.secondary};
    --color-text-accent: ${themeTokens.colors.text.accent};
    --color-text-positive: ${themeTokens.colors.text.positive};
    --color-text-negative: ${themeTokens.colors.text.negative};
    --color-text-disabled: ${themeTokens.colors.text.disabled};
    
    --color-brand-primary: ${themeTokens.colors.brand.primary};
    --color-brand-secondary: ${themeTokens.colors.brand.secondary};
    
    --spacing-xs: ${themeTokens.spacing.xs};
    --spacing-sm: ${themeTokens.spacing.sm};
    --spacing-md: ${themeTokens.spacing.md};
    --spacing-lg: ${themeTokens.spacing.lg};
    --spacing-xl: ${themeTokens.spacing.xl};
    --spacing-2xl: ${themeTokens.spacing['2xl']};
    --spacing-3xl: ${themeTokens.spacing['3xl']};
    
    --radius-sm: ${themeTokens.borderRadius.sm};
    --radius-md: ${themeTokens.borderRadius.md};
    --radius-lg: ${themeTokens.borderRadius.lg};
    --radius-xl: ${themeTokens.borderRadius.xl};
    --radius-2xl: ${themeTokens.borderRadius['2xl']};
    --radius-3xl: ${themeTokens.borderRadius['3xl']};
    --radius-full: ${themeTokens.borderRadius.full};
    
    --duration-fast: ${themeTokens.animation.duration.fast};
    --duration-normal: ${themeTokens.animation.duration.normal};
    --duration-slow: ${themeTokens.animation.duration.slow};
  }
`;