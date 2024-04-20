import {
  CancelablePromise,
  BiobuddyService,
  LoadConversationResponse,
  SaveMessageResponse,
  CheckBioBuddyEnabledResponse,
  SendQueryResponse,
} from 'src/api/client';

export function checkBioBuddyEnabled(): CancelablePromise<CheckBioBuddyEnabledResponse> {
  return BiobuddyService.checkBiobuddyEnabledApiV1BiobuddyCheckBiobuddyEnabledGet();
}

export function loadConversationApi(experimentId: string): CancelablePromise<LoadConversationResponse> {
  return BiobuddyService.loadConversationApiV1BiobuddyLoadConversationGet(experimentId);
}

export function saveMessageApi(experimentId: string, message: string): CancelablePromise<SaveMessageResponse> {
  return BiobuddyService.saveMessageApiV1BiobuddySaveMessagePost(experimentId, message);
}

export function sendQueryApi(experimentId: string, query: string): CancelablePromise<SendQueryResponse> {
  return BiobuddyService.sendQueryApiV1BiobuddySendQueryPost(experimentId, query);
}
