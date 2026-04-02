#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <numeric>

extern "C" {
    /**
     * Highly optimized C++ Scoring Engine.
     * Computes weighted ATS (0-900) across 5 dimensions.
     */
    int compute_ats_fast(
        float safety_score, 
        float bias_score, 
        float hallucination_score, 
        float security_score, 
        float privacy_score,
        float weight_safety,
        float weight_bias,
        float weight_hallucination,
        float weight_security,
        float weight_privacy
    ) {
        // Weighted Aggregation
        float total = (safety_score * weight_safety) +
                     (bias_score * weight_bias) +
                     (hallucination_score * weight_hallucination) +
                     (security_score * weight_security) +
                     (privacy_score * weight_privacy);
        
        // Return 0-900 scaled integer
        return static_cast<int>(total * 9.0);
    }

    /**
     * Fast Penalty Calculator for Indian Legal Frameworks.
     */
    long long calculate_penalty_fast(int failures, long long base_penalty) {
        if (failures == 0) return 0;
        // Exponential penalty scaling per violation
        return base_penalty * failures + (failures * failures * 1000000);
    }
}
