import type {SkillRun} from '../types.js';import {average} from '../utils/average.js';
export function calculateAvgDuration(runs:SkillRun[]):number{return average(runs.map(r=>r.durationMs));}
