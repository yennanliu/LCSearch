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
            <option value="difficulty-desc">Difficulty (Hard → Easy)</option>
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
      
      <button @click="handleDownloadCSV" class="download-button">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Download CSV
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
  emits: ['search', 'filter', 'sort', 'download-csv'],
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

    const handleDownloadCSV = () => {
      emit('download-csv')
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
      handleSort,
      handleDownloadCSV
    }
  }
}
</script>

<style scoped>
.search-bar {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 28px;
  padding: 2.5rem;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.08), 0 12px 24px rgba(0, 0, 0, 0.06);
  border: 2px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
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
  background: linear-gradient(135deg, rgba(255, 56, 92, 0.02) 0%, rgba(66, 165, 245, 0.02) 50%, rgba(102, 187, 106, 0.02) 100%);
  border-radius: 28px;
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
  padding: 24px 28px 24px 64px;
  font-size: 20px;
  font-weight: 500;
  border: none;
  border-radius: 20px;
  outline: none;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06), inset 0 1px 0 rgba(255, 255, 255, 0.6), 0 0 0 1px rgba(255, 56, 92, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-sizing: border-box;
  color: #222222;
}

.search-input::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

.search-input:focus {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 15px 45px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.8), 0 0 0 3px rgba(255, 56, 92, 0.15);
  transform: translateY(-3px);
}

.search-input:focus + .search-icon,
.search-input-container:hover .search-icon {
  color: #FF385C;
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
  gap: 0.75rem;
  font-weight: 700;
  color: #222222;
  font-size: 1.1rem;
  text-shadow: none;
}

.custom-select {
  position: relative;
  min-width: 200px;
}

.sort-select {
  width: 100%;
  padding: 16px 50px 16px 20px;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(10px);
  cursor: pointer;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  appearance: none;
  color: #222222;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(255, 56, 92, 0.06);
}

.sort-select:focus {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 10px 35px rgba(0, 0, 0, 0.12), 0 0 0 3px rgba(255, 56, 92, 0.15);
  transform: translateY(-2px);
}

.sort-select:hover {
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 56, 92, 0.1);
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
  color: #FF385C;
  transform: translateY(-50%) rotate(180deg);
}

.download-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 16px 24px;
  background: linear-gradient(135deg, #FF385C 0%, #FF6B98 100%);
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 6px 20px rgba(255, 56, 92, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.download-button:hover {
  background: linear-gradient(135deg, #FF2A52 0%, #FF5B88 100%);
  transform: translateY(-2px);
  box-shadow: 0 10px 35px rgba(255, 56, 92, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.2);
}

.download-button:active {
  transform: translateY(0);
  box-shadow: 0 4px 15px rgba(255, 56, 92, 0.3);
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
  
  .download-button {
    justify-content: center;
    padding: 14px 20px;
    font-size: 15px;
  }
}
</style>