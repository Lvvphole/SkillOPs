import {readFileSync,writeFileSync,existsSync,mkdirSync} from 'node:fs';import {dirname} from 'node:path';import type {SkillRun} from '../types.js';
function runsPath():string{return process.env.SKILLOPS_DATA_DIR?`${process.env.SKILLOPS_DATA_DIR}/runs.json`:'artifacts/runs.json';}
function read():SkillRun[]{const path=runsPath();return existsSync(path)?JSON.parse(readFileSync(path,'utf8')):[]}
export function insertRun(run:SkillRun):void{const path=runsPath();mkdirSync(dirname(path),{recursive:true});writeFileSync(path,JSON.stringify([...read(),run],null,2));}
export function selectRuns(skillId:string):SkillRun[]{return read().filter(r=>r.skillId===skillId);}
