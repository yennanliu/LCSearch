<template>
  <div class="search-bar">
    <div class="search-input-container">
      <div class="search-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 21L16.514 16.506L21 21ZM19 10.5C19 15.194 15.194 19 10.5 19C5.806 19 2 15.194 2 10.5C2 5.806 5.806 2 10.5 2C15.194 2 19 5.806 19 10.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search problems by title, tags, patterns, or companies..."
        class="search-input"
        @input="handleSearch"
      />
      <button 
        v-if="searchQuery"
        @click="clearSearch"
        class="clear-button"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
    
    <div class="controls-row">
      <div class="sort-section">
        <label for="sort-select" class="sort-label">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 6H21M7 12H17M11 18H13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Sort by
        </label>
        <div class="custom-select">
          <select 
            id="sort-select"
            v-model="currentSort" 
            @change="handleSort"
            class="sort-select"
          >
            <option value="recency">Latest First</option>
            <option value="difficulty">Difficulty (Easy → Hard)</option>
            <option value="title">Title (A → Z)</option>
            <option value="id">Problem ID</option>
          </select>
          <div class="select-arrow">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>
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
  emits: ['search', 'filter', 'sort'],
  setup(props, { emit }) {
    const searchQuery = ref('')
    const currentSort = ref('recency')
    
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

    const handleSort = () => {
      emit('sort', currentSort.value)
    }

    return {
      searchQuery,
      currentSort,
      allTags,
      allPatterns,
      allCompanies,
      handleSearch,
      clearSearch,
      handleFilter,
      handleSort
    }
  }
}
</script>

<style scoped>
.search-bar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.search-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
  border-radius: 24px;
  z-index: -1;
}

.search-input-container {
  position: relative;
  margin-bottom: 2rem;
}

.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  z-index: 2;
  transition: color 0.2s ease;
}

.search-input {
  width: 100%;
  padding: 20px 24px 20px 56px;
  font-size: 18px;
  font-weight: 500;
  border: none;
  border-radius: 16px;
  outline: none;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.4);
  transition: all 0.3s ease;
  box-sizing: border-box;
  color: #1f2937;
}

.search-input::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

.search-input:focus {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.4), 0 0 0 3px rgba(103, 126, 234, 0.1);
  transform: translateY(-2px);
}

.search-input:focus + .search-icon,
.search-input-container:hover .search-icon {
  color: #667eea;
}

.clear-button {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(239, 68, 68, 0.1);
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 8px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.clear-button:hover {
  background: rgba(239, 68, 68, 0.2);
  transform: translateY(-50%) scale(1.05);
}

.controls-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.sort-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sort-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: white;
  font-size: 0.95rem;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.custom-select {
  position: relative;
  min-width: 200px;
}

.sort-select {
  width: 100%;
  padding: 12px 44px 12px 16px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  cursor: pointer;
  outline: none;
  transition: all 0.3s ease;
  appearance: none;
  color: #374151;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.sort-select:focus {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15), 0 0 0 3px rgba(103, 126, 234, 0.1);
  transform: translateY(-1px);
}

.sort-select:hover {
  background: rgba(255, 255, 255, 1);
  transform: translateY(-1px);
}

.select-arrow {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  pointer-events: none;
  transition: all 0.2s ease;
}

.sort-select:focus + .select-arrow {
  color: #667eea;
  transform: translateY(-50%) rotate(180deg);
}

@media (max-width: 768px) {
  .search-bar {
    padding: 1.5rem;
    border-radius: 20px;
  }
  
  .search-input {
    padding: 16px 20px 16px 52px;
    font-size: 16px;
  }
  
  .controls-row {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .sort-section {
    justify-content: space-between;
  }
  
  .custom-select {
    min-width: auto;
    flex: 1;
    max-width: 200px;
  }
}
</style>