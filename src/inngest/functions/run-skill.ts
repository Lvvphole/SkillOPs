import {inngest} from '../client.js';import {runSkill} from '../../runs/runSkill.js';
export const runSkillFunction=inngest.createFunction({id:'run-skill'},{event:'skill/run'},async({event}:any)=>runSkill(event.data.skillId,event.data.input));
