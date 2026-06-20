import type {SkillRun} from '../types.js';import {insertRun} from '../db/queries.js';
export function logRunResult(run:SkillRun):SkillRun{insertRun(run);return run;}
