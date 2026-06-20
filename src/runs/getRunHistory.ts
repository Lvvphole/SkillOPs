import type {SkillRun} from '../types.js';import {selectRuns} from '../db/queries.js';
export function getRunHistory(skillId:string):SkillRun[]{return selectRuns(skillId);}
