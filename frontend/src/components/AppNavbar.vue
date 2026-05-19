<template>
  <header class="navbar">
    <RouterLink class="brand" to="/">LeetPrep-SQL</RouterLink>
    <nav class="nav-links" aria-label="Primary navigation">
      <RouterLink to="/">Dashboard</RouterLink>
      <RouterLink to="/problems">Problems</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid #d9e1ec;
  background: #ffffff;
  padding: 14px max(16px, calc((100vw - 1120px) / 2));
}

.brand {
  color: #101828;
  font-size: 18px;
  font-weight: 800;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-links a {
  border-radius: 8px;
  color: #526070;
  font-size: 14px;
  font-weight: 700;
  padding: 8px 12px;
}

.nav-links a.router-link-active {
  background: #e8f1ff;
  color: #1459b8;
}

@media (max-width: 560px) {
  .navbar {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
