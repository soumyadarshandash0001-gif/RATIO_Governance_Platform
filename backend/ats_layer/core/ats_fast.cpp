#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>

/**
 * C++ Production-Grade AI Governance Engine
 * Features:
 * 1. Trie-based Fast Pattern Matching (DSA)
 * 2. Weighted CIBIL Score Aggregation
 */

class TrieNode {
public:
    std::unordered_map<char, TrieNode*> children;
    bool isEndOfWord;

    TrieNode() : isEndOfWord(false) {}
};

class FastPatternMatcher {
private:
    TrieNode* root;

public:
    FastPatternMatcher() {
        root = new TrieNode();
    }

    void insert(std::string word) {
        TrieNode* curr = root;
        std::transform(word.begin(), word.end(), word.begin(), ::tolower);
        for (char c : word) {
            if (curr->children.find(c) == curr->children.end()) {
                curr->children[c] = new TrieNode();
            }
            curr = curr->children[c];
        }
        curr->isEndOfWord = true;
    }

    // Ultra-fast search (O(n) where n is text length)
    bool search_harmful_patterns(std::string text) {
        std::transform(text.begin(), text.end(), text.begin(), ::tolower);
        for (int i = 0; i < text.length(); i++) {
            TrieNode* curr = root;
            for (int j = i; j < text.length(); j++) {
                if (curr->children.find(text[j]) == curr->children.end()) break;
                curr = curr->children[text[j]];
                if (curr->isEndOfWord) return true;
            }
        }
        return false;
    }
};

extern "C" {
    static FastPatternMatcher matcher;

    /**
     * Seeds the C++ matcher with harmful patterns (C-string interface)
     */
    void add_pattern(const char* pattern) {
        matcher.insert(std::string(pattern));
    }

    /**
     * Executes ultra-fast evaluation of LLM response using Trie matching
     */
    bool evaluate_response_fast(const char* response) {
        return matcher.search_harmful_patterns(std::string(response));
    }

    /**
     * Highly optimized C++ Weighted Score aggregation.
     */
    int compute_cibil_optimized(
        float dimension_scores[], 
        float weights[], 
        int n
    ) {
        float total = 0;
        for(int i=0; i<n; i++) {
            total += dimension_scores[i] * weights[i];
        }
        return static_cast<int>(total * 9.0);
    }
}
