import type {SkillRun} from '../types.js';
export function calculateFalsePositiveRate(runs:SkillRun[]):number{const predicted=runs.filter(r=>r.predictedPositive);return predicted.length?predicted.filter(r=>!r.actualPositive).length/predicted.length:0;}
