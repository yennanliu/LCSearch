<template>
  <div v-if="totalPages > 1" class="pagination">
    <button 
      :disabled="currentPage === 1"
      @click="goToPage(currentPage - 1)"
      class="pagination-btn pagination-btn-nav"
      :class="{ disabled: currentPage === 1 }"
    >
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Previous
    </button>

    <div class="pagination-numbers">
      <template v-for="(page, index) in visiblePages" :key="index">
        <span
          v-if="page === '...'"
          class="pagination-ellipsis"
        >
          ...
        </span>
        <button
          v-else
          @click="goToPage(page)"
          class="pagination-btn pagination-btn-number"
          :class="{ active: page === currentPage }"
        >
          {{ page }}
        </button>
      </template>
    </div>

    <button 
      :disabled="currentPage === totalPages"
      @click="goToPage(currentPage + 1)"
      class="pagination-btn pagination-btn-nav"
      :class="{ disabled: currentPage === totalPages }"
    >
      Next
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <div class="pagination-info">
      <span class="page-info">
        Page {{ currentPage }} of {{ totalPages }}
      </span>
      <span class="items-info">
        {{ startItem }}-{{ endItem }} of {{ totalItems }} problems
      </span>
      <button
        v-if="totalPages > 15"
        @click="toggleShowAllPages"
        class="toggle-all-pages-btn"
      >
        {{ showAllPages ? 'Show Less' : 'Show All Pages' }}
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'ProblemPagination',
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalItems: {
      type: Number,
      required: true
    },
    itemsPerPage: {
      type: Number,
      default: 10
    }
  },
  emits: ['page-change'],
  setup(props, { emit }) {
    const showAllPages = ref(false)

    const totalPages = computed(() => Math.ceil(props.totalItems / props.itemsPerPage))

    const startItem = computed(() => (props.currentPage - 1) * props.itemsPerPage + 1)
    const endItem = computed(() => Math.min(props.currentPage * props.itemsPerPage, props.totalItems))

    const visiblePages = computed(() => {
      const pages = []
      const total = totalPages.value
      const current = props.currentPage

      // If show all pages is enabled or total pages is small, show all pages
      if (showAllPages.value || total <= 15) {
        for (let i = 1; i <= total; i++) {
          pages.push(i)
        }
        return pages
      }

      // For larger page counts, use smart pagination with ellipsis
      // Always show: first page, last page, current page, and 2 pages on each side of current

      // Always add first page
      pages.push(1)

      // Calculate range around current page
      const leftBound = Math.max(2, current - 2)
      const rightBound = Math.min(total - 1, current + 2)

      // Add ellipsis after first page if needed
      if (leftBound > 2) {
        pages.push('...')
      }

      // Add pages around current page
      for (let i = leftBound; i <= rightBound; i++) {
        if (i !== 1 && i !== total) {
          pages.push(i)
        }
      }

      // Add ellipsis before last page if needed
      if (rightBound < total - 1) {
        pages.push('...')
      }

      // Always add last page
      if (total > 1) {
        pages.push(total)
      }

      return pages
    })

    const toggleShowAllPages = () => {
      showAllPages.value = !showAllPages.value
    }

    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value && page !== props.currentPage) {
        emit('page-change', page)
      }
    }

    return {
      totalPages,
      startItem,
      endItem,
      visiblePages,
      goToPage,
      showAllPages,
      toggleShowAllPages
    }
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem 1rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(15px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.pagination-numbers {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
}

.pagination-ellipsis {
  color: #6b7280;
  font-weight: 600;
  padding: 0 8px;
  user-select: none;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  height: 44px;
}

.pagination-btn {
  padding: 10px 16px;
  border: 2px solid rgba(103, 126, 234, 0.2);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.8);
  color: #374151;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 14px;
}

.pagination-btn:hover:not(.disabled) {
  background: rgba(103, 126, 234, 0.1);
  border-color: rgba(103, 126, 234, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(103, 126, 234, 0.2);
}

.pagination-btn-nav {
  padding: 12px 18px;
  font-size: 15px;
}

.pagination-btn-number {
  width: 44px;
  height: 44px;
  padding: 0;
  justify-content: center;
  border-radius: 50%;
}

.pagination-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.pagination-btn.active:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5);
}

.pagination-btn.disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: rgba(255, 255, 255, 0.5);
  border-color: rgba(0, 0, 0, 0.1);
}

.pagination-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: #6b7280;
  font-size: 14px;
  text-align: center;
}

.page-info {
  font-weight: 600;
  color: #374151;
}

.items-info {
  font-weight: 400;
  color: #6b7280;
}

.toggle-all-pages-btn {
  margin-top: 0.75rem;
  padding: 8px 16px;
  border: 2px solid rgba(103, 126, 234, 0.3);
  border-radius: 8px;
  background: rgba(103, 126, 234, 0.1);
  color: #667eea;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-all-pages-btn:hover {
  background: rgba(103, 126, 234, 0.2);
  border-color: rgba(103, 126, 234, 0.5);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(103, 126, 234, 0.2);
}

@media (max-width: 768px) {
  .pagination {
    padding: 1.5rem 1rem;
  }
  
  .pagination-numbers {
    gap: 0.5rem;
  }
  
  .pagination-btn-nav {
    padding: 10px 14px;
    font-size: 14px;
  }
  
  .pagination-btn-nav span {
    display: none;
  }
  
  .pagination-btn-number {
    width: 40px;
    height: 40px;
  }
  
  .pagination-info {
    font-size: 13px;
  }
}
</style>