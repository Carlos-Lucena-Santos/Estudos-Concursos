import {filteredQuestions,validate} from './model.js';

export const officialSubjects = state => state.subjects.filter(subject => subject.kind === 'editalTopic');

// Somente vínculos explícitos com os assuntos oficiais entram na análise.
export function confirmedSubjectIds(state, question) {
 const available = new Set(officialSubjects(state).filter(s => s.disciplineId === question.disciplineId).map(s => s.id));
 return [...new Set(question.assuntoIds || [])].filter(id => available.has(id));
}

export function thematicSummary(state, filters = {}) {
 const questions = filteredQuestions(state, filters);
 const confirmed = questions.filter(q => confirmedSubjectIds(state, q).length > 0).length;
 return {total: questions.length, confirmed, pending: questions.length - confirmed};
}

export function subjectFrequency(state, filters = {}) {
 const questions = filteredQuestions(state, filters);
 const summary = thematicSummary(state, filters);
 return officialSubjects(state).filter(s => !filters.disciplineId || s.disciplineId === filters.disciplineId).map(subject => {
  const count = questions.filter(q => confirmedSubjectIds(state, q).includes(subject.id)).length;
  return {id: subject.id, name: subject.name, count, total: questions.length,
   percentage: questions.length ? 100 * count / questions.length : 0, pending: summary.pending};
 });
}

export function setQuestionSubjects(state, questionId, ids, observation = '') {
 const next = structuredClone(state);
 const question = next.questions.find(q => q.id === questionId);
 if (!question) throw Error('Questão inexistente.');
 if (!Array.isArray(ids)) throw Error('Selecione uma lista de assuntos oficiais.');
 question.assuntoIds = [...new Set(ids)];
 question.assuntosObservacao = observation;
 question.assuntosRevisadosEm = new Date().toISOString();
 return validate(next);
}
