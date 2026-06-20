import type {Incident} from './classifier.js';
export function evaluateIncident(i:Incident,label:string){const actualPositive=i.severity==='high'||i.customerImpact;return {success:(actualPositive&&label==='urgent')||(!actualPositive&&label==='standard'),actualPositive,actionTaken:label==='urgent'};}
