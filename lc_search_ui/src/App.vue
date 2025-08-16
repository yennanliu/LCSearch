<template>
  <div id="app">
    <header class="app-header">
      <h1>LeetCode Search</h1>
      <p>Find and filter LeetCode problems by difficulty, tags, patterns, and companies</p>
    </header>
    
    <main class="app-main">
      <SearchBar 
        @search="handleSearch" 
        @filter="handleFilter"
      />
      <ProblemList 
        :problems="filteredProblems"
        :loading="loading"
      />
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import SearchBar from './components/SearchBar.vue'
import ProblemList from './components/ProblemList.vue'

export default {
  name: 'App',
  components: {
    SearchBar,
    ProblemList
  },
  setup() {
    const problems = ref([])
    const loading = ref(true)
    const searchQuery = ref('')
    const filters = ref({
      difficulty: '',
      tags: [],
      patterns: [],
      companies: []
    })

    const loadProblems = async () => {
      try {
        const response = await fetch('/data/problems.json')
        problems.value = await response.json()
      } catch (error) {
        console.error('Failed to load problems:', error)
      } finally {
        loading.value = false
      }
    }

    const filteredProblems = computed(() => {
      let filtered = problems.value

      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(problem => 
          problem.title.toLowerCase().includes(query) ||
          problem.description?.toLowerCase().includes(query)
        )
      }

      if (filters.value.difficulty) {
        filtered = filtered.filter(problem => 
          problem.difficulty === filters.value.difficulty
        )
      }

      if (filters.value.tags.length > 0) {
        filtered = filtered.filter(problem => 
          filters.value.tags.some(tag => problem.tags.includes(tag))
        )
      }

      if (filters.value.patterns.length > 0) {
        filtered = filtered.filter(problem => 
          filters.value.patterns.some(pattern => problem.patterns.includes(pattern))
        )
      }

      if (filters.value.companies.length > 0) {
        filtered = filtered.filter(problem => 
          filters.value.companies.some(company => problem.companies.includes(company))
        )
      }

      return filtered
    })

    const handleSearch = (query) => {
      searchQuery.value = query
    }

    const handleFilter = (newFilters) => {
      filters.value = { ...filters.value, ...newFilters }
    }

    onMounted(loadProblems)

    return {
      filteredProblems,
      loading,
      handleSearch,
      handleFilter
    }
  }
}
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e9ecef;
}

.app-header h1 {
  color: #1976d2;
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
}

.app-header p {
  color: #666;
  margin: 0;
  font-size: 1.1rem;
}

.app-main {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>
