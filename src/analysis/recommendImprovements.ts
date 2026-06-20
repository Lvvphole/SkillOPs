import type {MetricSummary} from '../types.js';
export function recommendImprovements(summary:MetricSummary,explicitReview=false):string[]{if(summary.passed&&!explicitReview)return [];return summary.failures.map(f=>`Improve ${f} using deterministic evaluator evidence and add a new versioned skill file.`);}
