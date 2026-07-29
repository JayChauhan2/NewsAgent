const API_BASE_URL = '/api';

export async function fetchArticles() {
    try {
        const response = await fetch(`${API_BASE_URL}/articles`);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.warn("API endpoint unavailable, trying static /articles.json fallback", error);
    }
    
    try {
        const fallbackResponse = await fetch('/articles.json');
        if (fallbackResponse.ok) {
            return await fallbackResponse.json();
        }
    } catch (fallbackError) {
        console.error("Failed to fetch articles:", fallbackError);
    }
    return [];
}

export async function fetchAssignments() {
    try {
        const response = await fetch(`${API_BASE_URL}/assignments`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch assignments:", error);
        return [];
    }
}

export async function fetchArticle(id) {
    const articles = await fetchArticles();
    return articles.find(a => a.id === id);
}
export async function fetchAgentStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/agent_status.json`);
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.warn("API endpoint unavailable, trying static /agent_status.json fallback", error);
    }

    try {
        const fallbackResponse = await fetch('/agent_status.json');
        if (fallbackResponse.ok) {
            return await fallbackResponse.json();
        }
    } catch (err) {
        console.error("Failed to fetch agent status:", err);
    }
    return [];
}

export async function deleteArticle(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/articles/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return true;
    } catch (error) {
        console.error("Failed to delete article:", error);
        return false;
    }
}
