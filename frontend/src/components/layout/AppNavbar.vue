<template>
  <header class="app-navbar">
    <RouterLink class="brand" to="/" aria-label="LeetPrep-SQL dashboard">
      <span class="brand-mark">SQL</span>
      <span>LeetPrep-SQL</span>
    </RouterLink>

    <nav class="nav-links" aria-label="Primary navigation">
      <RouterLink to="/">Dashboard</RouterLink>
      <RouterLink to="/roadmap">Roadmap</RouterLink>
      <RouterLink to="/problems">Problems</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.app-navbar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  border-bottom: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  padding: 14px max(16px, calc((100vw - 1160px) / 2));
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text);
  font-size: 18px;
  font-weight: 900;
  white-space: nowrap;
}

.brand-mark {
  display: inline-grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: var(--radius-md);
  background: var(--color-primary);
  color: #ffffff;
  font-size: 12px;
  letter-spacing: 0;
}

.nav-links {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: var(--space-2);
}

.nav-links a {
  border-radius: var(--radius-md);
  color: var(--color-muted);
  font-size: 14px;
  font-weight: 850;
  padding: 9px 12px;
}

.nav-links a.router-link-active {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

@media (max-width: 560px) {
  .app-navbar {
    align-items: flex-start;
    flex-direction: column;
  }

  .nav-links {
    justify-content: flex-start;
    width: 100%;
  }
}
</style>
