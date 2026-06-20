declare const process:{env:Record<string,string|undefined>};
declare module 'node:fs'{export function readFileSync(path:string,enc:string):string;export function writeFileSync(path:string,data:string):void;export function existsSync(path:string):boolean;export function mkdirSync(path:string,opts?:{recursive?:boolean}):void;export function statSync(path:string):{size:number};}
declare module 'node:path'{export function dirname(path:string):string;}
declare module 'node:test'{const test:(name:string,fn:()=>void|Promise<void>)=>void;export default test;}
declare module 'node:assert/strict'{const assert:{equal:(a:unknown,b:unknown)=>void;deepEqual:(a:unknown,b:unknown)=>void;ok:(v:unknown)=>void};export default assert;}
