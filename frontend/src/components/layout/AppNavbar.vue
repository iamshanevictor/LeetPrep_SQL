<template>
  <header class="app-navbar" :class="{ 'is-workspace': workspace }">
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

<script setup>
defineProps({
  workspace: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
.app-navbar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  border-bottom: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  min-height: 45px;
  padding: 6px max(12px, calc((100vw - 1280px) / 2));
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text);
  font-size: 15px;
  font-weight: 850;
  white-space: nowrap;
}

.brand-mark {
  display: inline-grid;
  place-items: center;
  width: 26px;
  height: 26px;
  border-radius: var(--radius-sm);
  background: var(--color-primary);
  color: #ffffff;
  font-size: 11px;
  letter-spacing: 0;
}

.nav-links {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: var(--space-1);
}

.nav-links a {
  border-radius: var(--radius-sm);
  color: var(--color-muted);
  font-size: var(--font-sm);
  font-weight: 750;
  padding: 6px 9px;
}

.nav-links a.router-link-active {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.app-navbar.is-workspace {
  border-bottom-color: var(--color-border);
  background: rgba(255, 255, 255, 0.96);
}

.app-navbar.is-workspace .brand {
  color: var(--color-text);
}

.app-navbar.is-workspace .brand-mark {
  background: var(--color-primary);
  color: #ffffff;
}

.app-navbar.is-workspace .nav-links a {
  color: var(--color-text-muted);
}

.app-navbar.is-workspace .nav-links a.router-link-active {
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
