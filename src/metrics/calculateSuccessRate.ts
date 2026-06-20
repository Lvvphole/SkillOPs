import type {SkillRun} from '../types.js';
export function calculateSuccessRate(runs:SkillRun[]):number{return runs.length?runs.filter(r=>r.success).length/runs.length:0;}
