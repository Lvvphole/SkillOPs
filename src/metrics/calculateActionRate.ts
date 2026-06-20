import type {SkillRun} from '../types.js';
export function calculateActionRate(runs:SkillRun[]):number{return runs.length?runs.filter(r=>r.actionTaken).length/runs.length:0;}
