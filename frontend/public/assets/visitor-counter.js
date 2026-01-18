/**
 * Visitor Counter for Cloud Resume Challenge
 *
 * This script handles incrementing and displaying a visitor count by calling
 * a backend API (AWS API Gateway + Lambda or GCP Cloud Functions).
 *
 * Features:
 * - Graceful error handling
 * - Loading state management
 * - Support for multiple backend implementations (AWS/GCP)
 */

class VisitorCounter {
    /**
     * Initialize the visitor counter
     * @param {string} elementId - DOM element ID where count will be displayed
     * @param {string} apiEndpoint - API endpoint URL (will be set later)
     */
    constructor(elementId, apiEndpoint = null) {
        this.element = document.getElementById(elementId);
        this.apiEndpoint = apiEndpoint;

        if (!this.element) {
            console.error(`Element with ID '${elementId}' not found`);
            return;
        }

        // Only fetch count if API endpoint is configured
        if (this.apiEndpoint) {
            this.fetchVisitorCount();
        } else {
            console.warn('Visitor counter API endpoint not configured yet');
            this.displayPlaceholder();
        }
    }

    /**
     * Display a placeholder when API is not configured
     */
    displayPlaceholder() {
        this.element.textContent = '---';
        this.element.classList.add('counter-placeholder');
    }

    /**
     * Fetch visitor count from the API
     * Makes a POST request to increment and retrieve the count
     */
    async fetchVisitorCount() {
        try {
            // Show loading state
            this.showLoading();

            // Make POST request to API
            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                // Some APIs might need additional configuration
                mode: 'cors',
            });

            // Check if response is ok
            if (!response.ok) {
                throw new Error(`API responded with status: ${response.status}`);
            }

            // Parse JSON response
            const data = await response.json();

            // Validate response format
            if (typeof data.count !== 'number') {
                throw new Error('Invalid response format: missing count');
            }

            // Display the count
            this.displayCount(data.count);

        } catch (error) {
            console.error('Error fetching visitor count:', error);
            this.displayError();
        }
    }

    /**
     * Show loading state
     */
    showLoading() {
        this.element.textContent = 'Loading...';
        this.element.classList.add('counter-loading');
    }

    /**
     * Display the visitor count
     * @param {number} count - The visitor count to display
     */
    displayCount(count) {
        this.element.classList.remove('counter-loading', 'counter-error', 'counter-placeholder');
        this.element.classList.add('counter-loaded');

        // Format count with commas for readability (e.g., 1,234)
        const formattedCount = count.toLocaleString();
        this.element.textContent = formattedCount;
    }

    /**
     * Display error state with fallback message
     * Degrades gracefully without breaking the page
     */
    displayError() {
        this.element.classList.remove('counter-loading', 'counter-loaded', 'counter-placeholder');
        this.element.classList.add('counter-error');
        this.element.textContent = 'N/A';
        this.element.title = 'Unable to load visitor count';
    }

    /**
     * Update the API endpoint (useful for switching between AWS/GCP)
     * @param {string} newEndpoint - New API endpoint URL
     */
    setEndpoint(newEndpoint) {
        this.apiEndpoint = newEndpoint;
        if (this.apiEndpoint) {
            this.fetchVisitorCount();
        }
    }
}

// Initialize the counter when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Configuration object - update this with your actual API endpoint
    const config = {
        // AWS API Gateway endpoint (custom domain)
        awsEndpoint: 'https://api.danphillipsonline.com/counter',

        // GCP Cloud Functions endpoint (update when ready)
        gcpEndpoint: 'https://api.danphillips.cloud/',

        // Set which backend to use: 'aws' or 'gcp'
        activeBackend: 'gcp'
    };

    // Select the appropriate endpoint based on configuration
    const endpoint = config.activeBackend ===gcp'
        ? config.awsEndpoint
        : config.gcpEndpoint;

    // Initialize the visitor counter
    window.visitorCounter = new VisitorCounter('visitor-count', endpoint);
});
