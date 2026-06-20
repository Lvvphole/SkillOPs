export type Incident={id:string;description:string;severity:'low'|'medium'|'high';customerImpact:boolean};
export function classifyIncident(i:Incident){const urgent=i.severity==='high'||i.customerImpact;return {label:urgent?'urgent':'standard',predictedPositive:urgent};}
