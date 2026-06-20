import type {SkillChange} from '../types.js';import {verifyEvidence} from './verifyEvidence.js';import {verifyProposedChanges} from './verifyProposedChanges.js';
export function approveSkillUpdate(c:SkillChange){const evidence=verifyEvidence(c.evidencePaths);const changes=verifyProposedChanges(c);return {approved:evidence.approved&&changes.approved,evidence,changes};}
