export type SkillRun={id:string;skillId:string;startedAt:string;endedAt:string;durationMs:number;success:boolean;predictedPositive:boolean;actualPositive:boolean;actionTaken:boolean;notes?:string};
export type Thresholds={minSuccessRate:number;maxAvgDurationMs:number;maxFalsePositiveRate:number;minActionRate:number};
export type MetricSummary={successRate:number;avgDurationMs:number;falsePositiveRate:number;actionRate:number;passed:boolean;failures:string[]};
export type SkillChange={skillId:string;fromVersion:string;toVersion:string;proposedContent:string;evidencePaths:string[];reason:string};
