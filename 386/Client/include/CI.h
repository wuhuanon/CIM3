    int EnumOrder(dword_t **ppOrderID, dword_t *pCount);
    int QueryOrderInfo(dword_t orderID, CI_order_info_t *pOrderInfo);
    int DelOrder(dword_t orderID);

    int EnumOrderDataFile(dword_t orderID, dword_t **ppFileID, dword_t *pCount);
    int QueryOrderDataFileInfo(dword_t orderID, dword_t fileID, CI_magnetic_file_info_t* pInfo);
    int QueryOrderDataFilePAN(dword_t orderID, dword_t fileID, dword_t startIdx, word_t count, CI_PAN_info_t **ppInfo);
    int DelOrderDataFile(dword_t orderID, dword_t fileID);

    //机台管理
    int EnumMachine(dword_t **ppDevID, dword_t *pCount);
    int NewMachine(const CI_device_info_t *pInfo, dword_t *pDevID);
    int UpdateMachine(dword_t devID, const CI_device_desc_t *pInfo);
    int QueryMachine(dword_t devID, CI_device_info_t *pInfo);
    int DelMachine(dword_t devID);

    //任务创建
    int NewJobBegin(dword_t orderID, const CI_job_desc_t* desc);
    int NewJobDataFile(dword_t fileID);
    int NewJobUpload(word_t ctPAN, dword_t *pID);
    int NewJobCommit(dword_t *pJobID);
    int NewJobAbort();

    //任务查询
    int EnumJob(dword_t orderID, dword_t **ppJobID, dword_t *pCount);
    int QueryJobInfo(const job_ref_t *pJobRef, CI_job_info_t *pJobInfo);
    int QueryTaskInfo(const job_ref_t *pJobRef, CI_task_runtime_info_t *pTaskInfo);
    int QueryIssueInfo(const job_ref_t *pJobRef, CI_job_issue_info_t *pTaskInfo);

    int StartTask(const job_ref_t *pJobRef, dword_t devID, const kcv_t *pKMC, dword_t diversifyKMC);
    int StopTask(const job_ref_t *pJobRef);
    int FinishTask(const job_ref_t *pJobRef, const CI_job_desc_t* desc);
    int GetTaskDevicePort(const job_ref_t *pJobRef, dword_t *pDevID, word_t *pPort);

    int QueryRecordExistInActiveJob(dword_t orderID, word_t count, dword_t *pPANID);
    int QueryLogExistInFinishedJob(dword_t orderID, word_t count, dword_t *pPANID);
    int QueryRecordInActiveJob(dword_t orderID, dword_t panID, CI_job_record_t **ppRecord, dword_t *pCount);
    int QueryLoggedRecordInFinishedJob(dword_t orderID, dword_t panID, CI_job_record_t **ppRecord, dword_t *pCount);

    int QueryLog(const job_ref_t *pJobRef, dword_t startIdx, word_t count, PAN_CI_log_t **ppInfo);

    int FetchOrderEvent(CI_order_event_t **ppEvent, dword_t *pCount);
    int FetchTaskEvent(dword_t orderID, CI_task_event_t **ppEvent, dword_t *pCount);
    int FetchFileEvent(dword_t orderID, CI_file_event_t **ppEvent, dword_t *pCount);
