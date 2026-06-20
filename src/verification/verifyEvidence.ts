import {existsSync,statSync} from 'node:fs';
export function verifyEvidence(paths:string[]):{approved:boolean;missing:string[]}{const missing=paths.filter(p=>!existsSync(p)||statSync(p).size===0);return {approved:missing.length===0,missing};}
