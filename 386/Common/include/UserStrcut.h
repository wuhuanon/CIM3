#ifndef __USER_MGMT_H_INCLUDED_6303474__
#define __USER_MGMT_H_INCLUDED_6303474__

#include <typedef.h>
#include <agent.h>
#include <constants.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct
{
	word_t nameLen;
	char nameBuf[USER_GROUP_NAME_LENGTH_MAX];
	dword_t priHigh;
	dword_t priLow;	
}fcps_user_group_info_t;

int	UM_NewUserGroup(agent_t pAgent, char* name, word_t length, fcps_user_group_info_t info);
int	UM_DelUserGroup(agent_t pAgent, char* name, word_t length);
int	UM_UpdateUserGroup(agent_t pAgent, char* name, word_t length,  fcps_user_group_info_t info);
int	UM_EnumUserGroup(agent_t pAgent, fcps_user_group_query_info_t** ppUserGroupInfo, dword_t* pUserGroupCout);

typedef struct
{	
{
	word_t userNameLen;
	char userName[USER_NAME_LENGTH_MAX];
	word_t pinLen;
	char pin[USER_PIN_LENGTH_MAX];
	word_t gnLen;
	char groupName[USER_GROUP_NAME_LENGTH_MAX];
	unsigned short pinValidDayCount;
	int status;
	int authType;	
}fcps_user_info_t;

typedef struct
{
	word_t userNameLen;
	char userName[USER_NAME_LENGTH_MAX];
	word_t groupNameLen;
	char groupName[USER_GROUP_NAME_LENGTH_MAX];
  	 unsigned short pinValidDayCount;
  	 unsigned short pinValidDayCountRemain;
   	int status;
   	int authType;
}fcps_user_query_info_t;

int	UM_newUser(agent_t pAgent, char* name, word_t len, fcps_user_info_t* pUserInfo);
int	UM_delUser(agent_t pAgent, char* name, word_t len);
int	UM_updateUser(agent_t pAgent, char* name, word_t len, fcps_user_info_t* pUserInfo);
int	UM_EnumUser(agent_t pAgent, char* groupName,  word_t gnLen, fcps_user_query_info_t** ppUserQueryInfo, dword_t * pUserCount);

int	UM_UserLogIn(agent_t pAgent, char* name, word_t nameLen, char* pin, word_t pinLen);
int	UM_UserLogOut(agent_t pAgent);
int	UM_UserUpdatePin(agent_t pAgent, char* oldPin,word_t oldPinLen, char* newPin, word_t newPinLen);

#ifdef __cplusplus
}
#endif

#endif
