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
        @sort="handleSort"
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
      companies: [],
      sortBy: 'recency' // recency, difficulty, title
    })

    const sortProblems = (problems, sortBy) => {
      const sorted = [...problems]
      
      switch (sortBy) {
        case 'recency':
          return sorted.sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded))
        case 'difficulty': {
          const difficultyOrder = { 'Easy': 1, 'Medium': 2, 'Hard': 3 }
          return sorted.sort((a, b) => difficultyOrder[a.difficulty] - difficultyOrder[b.difficulty])
        }
        case 'title':
          return sorted.sort((a, b) => a.title.localeCompare(b.title))
        case 'id':
          return sorted.sort((a, b) => a.id - b.id)
        default:
          return sorted.sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded))
      }
    }

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

      // Text search - search in title, description, and tags
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase().trim()
        
        filtered = filtered.filter(problem => {
          const titleMatch = problem.title.toLowerCase().includes(query)
          const descMatch = problem.description?.toLowerCase().includes(query) || false
          const tagMatch = problem.tags.some(tag => tag.toLowerCase().includes(query))
          const patternMatch = problem.patterns.some(pattern => pattern.toLowerCase().includes(query))
          const companyMatch = problem.companies.some(company => company.toLowerCase().includes(query))
          
          return titleMatch || descMatch || tagMatch || patternMatch || companyMatch
        })
      }

      // Difficulty filter
      if (filters.value.difficulty) {
        filtered = filtered.filter(problem => 
          problem.difficulty === filters.value.difficulty
        )
      }

      // Tags filter (OR logic - match any selected tag)
      if (filters.value.tags.length > 0) {
        filtered = filtered.filter(problem => 
          filters.value.tags.some(tag => problem.tags.includes(tag))
        )
      }

      // Patterns filter (OR logic - match any selected pattern)
      if (filters.value.patterns.length > 0) {
        filtered = filtered.filter(problem => 
          filters.value.patterns.some(pattern => problem.patterns.includes(pattern))
        )
      }

      // Companies filter (OR logic - match any selected company)
      if (filters.value.companies.length > 0) {
        filtered = filtered.filter(problem => 
          filters.value.companies.some(company => problem.companies.includes(company))
        )
      }

      // Apply sorting
      return sortProblems(filtered, filters.value.sortBy)
    })

    const handleSearch = (query) => {
      searchQuery.value = query
    }

    const handleFilter = (newFilters) => {
      filters.value = { ...filters.value, ...newFilters }
    }

    const handleSort = (sortBy) => {
      filters.value.sortBy = sortBy
    }

    onMounted(loadProblems)

    return {
      filteredProblems,
      loading,
      handleSearch,
      handleFilter,
      handleSort
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
