<script>
  let queryText = '';
  let responseData = null;
  let isLoading = false;
  let errorMessage = '';
  let copied = false;
  const API_BASE = import.meta.env.PUBLIC_API_URL || 'http://127.0.0.1:8000';

  async function submitQuery() {
    if (!queryText.trim()) return;
    
    isLoading = true;
    errorMessage = '';
    responseData = null;

    try {
      const response = await fetch(`${API_BASE}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: queryText })
      });

      if (!response.ok) {
        const errPayload = await response.json();
        throw new Error(errPayload.detail || 'Server encountered an issue processing policy data.');
      }

      responseData = await response.json();
    } catch (err) {
      errorMessage = err.message;
    } finally {
      isLoading = false;
    }
  }

  function copyToClipboard() {
    if (!responseData) return;
    navigator.clipboard.writeText(responseData.answer);
    copied = true;
    setTimeout(() => { copied = false; }, 2000);
  }
</script>

<div class="dashboard-wrapper">
  <form on:submit|preventDefault={submitQuery} class="input-card">
    <div class="input-group">
      <input
        type="text"
        bind:value={queryText}
        placeholder="Search public policy archives (e.g., Housing, Floods, Transport)..."
        disabled={isLoading}
        aria-label="Policy Query"
      />
      <button type="submit" disabled={isLoading || !queryText.trim()}>
        {#if isLoading}
          <span class="spinner"></span>
          Seeking...
        {:else}
          Run Query
        {/if}
      </button>
    </div>
  </form>


  {#if errorMessage}
    <div class="state-card error-card">
      <div class="icon">⚠︎</div>
      <div class="content">
        <h4>Pipeline Resolution Failure</h4>
        <p>{errorMessage}</p>
      </div>
    </div>
  {/if}

  {#if isLoading}
    <div class="state-card loading-card">
      <div class="skeleton-line short animate-pulse"></div>
      <div class="skeleton-block animate-pulse"></div>
    </div>
  {/if}

  {#if responseData && !isLoading}
    <div class="result-card">
      <div class="result-header">
        <div class="meta-tag">
          <span class="dot"></span>
          Sources Tracked: <strong>{responseData.sources_found}</strong>
        </div>
        <button class="copy-btn" on:click={copyToClipboard}>
          {copied ? '✓ Copied' : 'Copy Output'}
        </button>
      </div>

      <div class="output-viewport">
        <div class="viewport-label">SYSTEM_REPLY</div>
        <p class="viewport-text">{responseData.answer}</p>
      </div>
    </div>
  {/if}
</div>

<style>
 :global(html) {
    --bg-main: #fafafa;
    --card-bg: #ffffff;
    --border-color: #e4e4e7; 
    --text-primary: #09090b; 
    --text-muted: #71717a;  
    --accent: #4f46e5;       
    --accent-glow: rgba(79, 70, 229, 0.08);
    --error-bg: #fef2f2;
    --error-border: #f87171;
  }

  .dashboard-wrapper {
    width: 100%;
    max-width: 48rem;
    margin: 0 auto;
    font-family: ui-sans-serif, system-ui, sans-serif;
  }

  /* form and input card styling */
  .input-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 6px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .input-card:focus-within {
    border-color: var(--accent);
    box-shadow: 0 0 15px var(--accent-glow);
  }

  .input-group {
    display: flex;
    gap: 8px;
  }

  input {
    flex: 1;
    background: transparent;
    border: none;
    padding: 12px 16px;
    color: var(--text-primary);
    font-size: 0.95rem;
    outline: none;
  }

  input::placeholder {
    color: #a1a1aa;
  }

  button {
    background: var(--text-primary);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 0 20px;
    font-weight: 600;
    font-size: 0.875rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: background-color 0.2s;
  }

  button:hover:not(:disabled) {
    background: #27272a;
  }

  button:disabled {
    background: #f4f4f5;
    color: #a1a1aa;
    cursor: not-allowed;
  }

  /* status cards, error/loading*/
  .state-card {
    margin-top: 24px;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid var(--border-color);
    background: var(--card-bg);
  }

  .error-card {
    display: flex;
    gap: 16px;
    background: var(--error-bg);
    border-color: var(--error-border);
  }

  .error-card .icon {
    font-size: 1.25rem;
  }

  .error-card h4 {
    margin: 0 0 4px 0;
    color: #991b1b;
    font-size: 0.9rem;
    font-weight: 600;
  }

  .error-card p {
    margin: 0;
    color: #b91c1c;
    font-size: 0.875rem;
  }

  /* output result */
  .result-card {
    margin-top: 24px;
    animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .result-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding: 0 4px;
  }

  .meta-tag {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.8rem;
    color: var(--text-muted);
  }

  .dot {
    width: 6px;
    height: 6px;
    background: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(16, 185, 129, 0.4);
  }

  .copy-btn {
    background: var(--card-bg);
    color: var(--text-muted);
    border: 1px solid var(--border-color);
    padding: 6px 12px;
    font-size: 0.75rem;
    border-radius: 6px;
  }

  .copy-btn:hover {
    background: #f4f4f5;
    color: var(--text-primary);
  }

  .output-viewport {
    background: #ffffff;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    position: relative;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  }

  .viewport-label {
    font-family: monospace;
    font-size: 0.7rem;
    color: #a1a1aa;
    letter-spacing: 0.1em;
    margin-bottom: 16px;
    border-bottom: 1px dashed var(--border-color);
    padding-bottom: 8px;
  }

  .viewport-text {
    margin: 0;
    font-size: 0.925rem;
    color: var(--text-primary);
    line-height: 1.6;
    white-space: pre-line;
  }

  /* loading animation */
  .spinner {
    width: 14px;
    height: 14px;
    border: 2px solid #e4e4e7;
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
  }

  .skeleton-line {
    height: 12px;
    background: #f4f4f5;
    border-radius: 4px;
    margin-bottom: 12px;
  }
  .skeleton-line.short { width: 30%; }
  .skeleton-block { height: 80px; background: #f4f4f5; border-radius: 8px; }

  .animate-pulse {
    animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }

  @keyframes spin { to { transform: rotate(360deg); } }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .4; } }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
</style>
