#ifndef __DP_H_58638462_INCLUDED__
#define __DP_H_58638462_INCLUDED__

#include <typedef.h>
#include <AgentC.h>
#include <dpdata_struct.h>
#include <CI_struct.h>

enum
{
    DP_FILE_STATUS_READY = 1,
    DP_FILE_STATUS_PARTIAL_OK = 2,
    DP_FILE_STATUS_FAILED = 3,
    DP_FILE_STATUS_ALL_OK = 4,
    DP_FILE_STATUS_FROZEN = 5,
    DP_FILE_STATUS_DELETED = 6,
    DP_FILE_STATUS_DP = 7,
};

#ifdef __cplusplus
extern "C" {
#endif

int DP_UploadBegin(agentc_t* pAgent, const DP_file_upload_info_t* pFileUploadInfo);
int DP_Upload(agentc_t* pAgent, const PAN_name_t* pPAN, const decode_record_t* pMagnICRecord, const char* pMagnSRecord, word_t BufSize);
int DP_UploadEnd(agentc_t* pAgent);

int DP_StartTask(agentc_t *pAgent, const magnetic_file_name_t* pFileName, const c_template_info* pTemplate, dword_t derivationAlg, dword_t certSerialInitial, dword_t *subErr);
int DP_StopTask(agentc_t *pAgent, const magnetic_file_name_t* pFileName);

int DP_DataFileDel(agentc_t *pAgent, const magnetic_file_name_t* pFileName);
int DP_DataFileFrozen(agentc_t *pAgent, const magnetic_file_name_t* pFileName);

int DP_EnumDataFile(agentc_t *pAgent, magnetic_file_name_t **ppFileName, dword_t* pCount);
int DP_GetFileEvent(agentc_t *pAgent,  mag_file_event_t **ppFileEvent, dword_t* pCount);
int DP_GetFileInfoStatus(agentc_t *pAgent, const magnetic_file_name_t *pFileName, magnetic_file_query_info* pInfo);
int DP_GetFileTemplate(agentc_t *pAgent, const magnetic_file_name_t *pFileName, c_template_info* pTemplate);

int DP_GetTaskStatus(agentc_t *pAgent, dword_t *pStatus, task_info_t** ppTask, dword_t *pCountRunning, dword_t *pCountBlocked);
int DP_SetMaxThread(agentc_t* pAgent, dword_t count);
int DP_GetMaxThread(agentc_t* pAgent, dword_t *pCount);
int DP_AdjustPriority(agentc_t* pAgent, const magnetic_file_name_t *pCardDataName, int op);
int DP_SuspendAll(agentc_t* pAgent);
int DP_ResumeAll(agentc_t* pAgent);

int DP_QueryDataFileBegin(agentc_t *pAgent, const magnetic_file_name_t *pFileName, c_template_info *pTemplate, CI_key_base_info_t *pKey);
int DP_QueryDataFile(agentc_t *pAgent, dword_t idx, byte_t** pBuf, dword_t *pSize);
int DP_QueryDataFileEnd(agentc_t *pAgent);

#ifdef __cplusplus
}
#endif

#endif
