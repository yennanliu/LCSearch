<template>
  <div class="search-bar">
    <div class="search-input-container">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search problems by title or description..."
        class="search-input"
        @input="handleSearch"
      />
      <button 
        v-if="searchQuery"
        @click="clearSearch"
        class="clear-button"
      >
        ×
      </button>
    </div>
    
    <FilterPanel 
      :all-tags="allTags"
      :all-patterns="allPatterns"
      :all-companies="allCompanies"
      @filter="handleFilter"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import FilterPanel from './FilterPanel.vue'

export default {
  name: 'SearchBar',
  components: {
    FilterPanel
  },
  emits: ['search', 'filter'],
  setup(props, { emit }) {
    const searchQuery = ref('')
    
    const allTags = [
      'Array', 'Hash Table', 'String', 'Dynamic Programming', 'Math',
      'Depth-First Search', 'Breadth-First Search', 'Binary Search',
      'Two Pointers', 'Greedy', 'Sliding Window', 'Linked List',
      'Stack', 'Queue', 'Tree', 'Graph', 'Heap', 'Sorting',
      'Recursion', 'Divide and Conquer', 'Backtracking', 'Trie',
      'Union Find', 'Matrix', 'Prefix Sum', 'Memoization'
    ]
    
    const allPatterns = [
      'Two Pointers', 'Sliding Window', 'Hash Map', 'Binary Search',
      'DFS', 'BFS', 'DP', 'Greedy', 'Backtracking', 'Union Find',
      'Kadane\'s Algorithm', 'Prefix Sum', 'Sorting', 'Recursion',
      'Fibonacci', 'Fast & Slow Pointers', 'Merge Intervals',
      'Cyclic Sort', 'In-place Reversal', 'Tree Traversal'
    ]
    
    const allCompanies = [
      'Google', 'Amazon', 'Microsoft', 'Facebook', 'Apple',
      'Netflix', 'Uber', 'LinkedIn', 'Adobe', 'Bloomberg',
      'Tesla', 'Airbnb', 'Spotify', 'Dropbox', 'Twitter',
      'Salesforce', 'Oracle', 'IBM', 'Intel', 'Nvidia'
    ]

    const handleSearch = () => {
      emit('search', searchQuery.value)
    }

    const clearSearch = () => {
      searchQuery.value = ''
      emit('search', '')
    }

    const handleFilter = (filters) => {
      emit('filter', filters)
    }

    return {
      searchQuery,
      allTags,
      allPatterns,
      allCompanies,
      handleSearch,
      clearSearch,
      handleFilter
    }
  }
}
</script>

<style scoped>
.search-bar {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e9ecef;
}

.search-input-container {
  position: relative;
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 16px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.search-input:focus {
  border-color: #1976d2;
}

.clear-button {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 20px;
  color: #666;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease;
}

.clear-button:hover {
  background-color: #f5f5f5;
}
</style>