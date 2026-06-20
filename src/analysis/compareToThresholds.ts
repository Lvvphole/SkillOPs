import type {MetricSummary} from '../types.js';
export function compareToThresholds(summary:MetricSummary){return {passed:summary.passed,failures:[...summary.failures]};}
