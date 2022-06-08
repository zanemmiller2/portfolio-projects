#include <sys/wait.h> // for waitpid
#include <sys/types.h>
#include <fcntl.h>    // for open,
#include <stdio.h>    // for printf and perror
#include <stdlib.h>   // for exit
#include <unistd.h>   // for execv, getpid, fork
#include <string.h>   // for string operations (strtok)
#include <stdbool.h>  // for background bool value
#define MAXARGS 512   // first argument is command
#define MAXSTRING 2048
#define MAXFILELEN 256

void get_cl_input(char* get_input[512], char in_file_name[], char out_file_name[], int* background_stat);
void change_directory(char* new_path);
void execute_command(char* user_input[], int* exit_status, int* background_status, char in_file_name[], char out_file_name[]);

int main()
{
  char* user_input[512];      // array of 512 pointers - max number of args
  char in_file_name[256];     // max path name length
  char out_file_name[256];    // max file name length
  // int parent_pid = getpid();
  int exit_stat = 0;
  int background_stat = 0;
  char temp_arr[256];
  user_input[0] = temp_arr;

  do
  {
    for (int i = 0; i < 256; i++)
    {
      in_file_name[i] = '\0';
      out_file_name[i] = '\0';
    }

    // char* cwd_path;
    // getwd(cwd_path);
    printf(": ");
    fflush(stdout);

    // Get user input from stdin
    get_cl_input(user_input, in_file_name, out_file_name, &background_stat);

    // Check for comments and empty lines --- IGNORE
    if((user_input[0][0] == '#') || (user_input[0][0] == '\0'))
    {
      continue;
    }

    /* ----- Built ins ----- */

    /* Exit */ // --- need a better way to test exitstuff also enters exit
    if(strncmp(&user_input[0][0], "exit", 4) == 0)
    {
      // kill all processes ??
      exit(0); // correct value?
    }

    /* cd */ // ---- need to find a better way to test cdm also enters cd
    else if(strncmp(&user_input[0][0], "cd", 2) == 0)
    {
      //change_directory(user_input[1]);
      chdir(user_input[1]);
    } 

    /* Status */ // ---- need to find a better way to test statususshsh also enters status
    else if(strncmp(&user_input[0][0], "status", 6) == 0)
    {
      if(WIFSIGNALED(background_stat))
      {
        printf("Termination by signal %d\n", WTERMSIG(exit_stat));
        fflush(stdout);
      }
      else
      {
        printf("Termination by status %d\n", WEXITSTATUS(exit_stat));
        fflush(stdout);
      }
    }

    /* Non Built-Ins */
    else
    {
      execute_command(user_input, &exit_stat, &background_stat, in_file_name, out_file_name);
    }
    

    }
    while (strncmp(&user_input[0][0], "exit", 4) != 0);
    }

/*------------------------------------------------------------------------------------------*/
//  Get/Parse user input from command line 
//    
//
/*------------------------------------------------------------------------------------------*/
void get_cl_input(char* get_input[], char in_file_name[], char out_file_name[], int* background_stat){
  // temp array for getting input from stdin
  char temp_input[2048];    // max input length as specified
  char* token;

  // get input
  fgets(temp_input, 2048, stdin);

  // strip out new line char
  int temp_index = strlen(temp_input);
  if(temp_input[temp_index - 1] == '\n')
  {
    // replace \n with \0
    temp_input[temp_index - 1] = '\0';
  }
  token = strtok(temp_input, " \n");
  for (int i = 0; i < temp_index; i++)
  {
    if(!token)
    {
      return;
    }

    // input redirection
    else if(strcmp(token, "<") == 0)
    {
      // next token is in_file name
      token = strtok(NULL, " \n");
      strcpy(in_file_name, token);
    }

    // output redirection
    else if(strcmp(token, ">") == 0)
    {
      // next token is out_file name
      token = strtok(NULL, " \n");
      strcpy(out_file_name, token);
    }

    // background process  
    else if(strcmp(token, "&") == 0)
    {
      // Background command and no input/output redirection
      if(in_file_name[0] == '\0')
      {
        strcpy(in_file_name, "/dev/null");
      }
      if(out_file_name[0] == '\0')
      {
        strcpy(out_file_name, "/dev/null");
      }
      *background_stat = 1;
    }

    // commands + [args...]
    else 
    {
      // Handle $$ expansion (as of now assuming only 2 chars at end)
      char temp_orig[256];
      char temp_build[256];
      strcpy(temp_orig, token);
      if(strstr(temp_orig, "$$"))
      {
        for(size_t j = 0; j < strlen(token); j++)
        {
          if(temp_orig[j] == '$' && temp_orig[j+1] == '$')
          {
            snprintf(&temp_build[j], 256, "%d", getpid());
            fflush(stdout);
            break;
          }
          else
          {
            temp_build[j] = temp_orig[j];
          }
          temp_build[j+1] = '\0';
        }
        get_input[i] = &temp_build[0];
      }
      // No $$ in string
      else
      {
        // null terminate string
        get_input[i] = token;
      }
      // printf("Command entered: %s\n", get_input[i]);
      // fflush(stdout);
    }
    token = strtok(NULL, " \n");
  }
  return;
}

/*------------------------------------------------------------------------------------------*/
//  Execute commands not built in
//    
//
/*------------------------------------------------------------------------------------------*/
void execute_command(char* user_input[], int* exit_status, int* background_status, char in_file_name[], char out_file_name[]){
  int childStatus; 
  int input_fd, new_in_fd, output_fd, new_out_fd;
  
  // fork a new process
  pid_t child_pid = fork();
  switch(child_pid)
  {
    case -1: 
            perror("fork()\n");
            fflush(stdout);
            *exit_status = 1;
            exit(1);
    
    case 0:
          printf("Child(%d) running %s command\n", getpid(), user_input[0]);
          fflush(stdout);

          /* --- Handle input/output redirection --- */
          // get the file desriptor of the input_file (input redirected)
          if (strncmp(&in_file_name[0], "\0", 1) != 0)
          {
            printf("In name: %s\n", in_file_name);
            fflush(stdout);
            input_fd = open(in_file_name, O_RDONLY, 00600);

            // file open error
            if(input_fd == -1)
            {
              printf("open() failed on \"%s\"\n", in_file_name);
              fflush(stdout);
              perror("Error");
              fflush(stdout);
              // Set exit status but dont exit shell
              *exit_status = 1;
              exit(1);          // break???
            }

            // update stdin file descriptor
            int result = dup2(input_fd, 0);

            // test reassignment successful
            if(result == -1)
            {
              perror("in error at dup");
              fflush(stdout);
              exit(1);
            }
          }
          // get the file desriptor of the output_file (output redirected)
          if(strncmp(&out_file_name[0], "\0", 1) != 0)
          {
            printf("Out name: %s\n", out_file_name);
            fflush(stdout);
            output_fd = open(out_file_name, O_WRONLY | O_CREAT | O_TRUNC, 00600);

            // file open error
            if(output_fd == -1)
            {
              printf("open() failed on \"%s\"\n", out_file_name);
              fflush(stdout);
              perror("Error");
              fflush(stdout);
              // Set exit status but dont exit shell
              *exit_status = 1;
              exit(1);
            }

            // update stdout file descriptor -- dup2 returns the new fd
            int result = dup2(output_fd, 1);
            // test reassignment successful
            if(result == -1)
            {
              perror("out error at dup");
              fflush(stdout);
              exit(1);
            }
          }
          
          execvp(user_input[0], user_input);
          exit(1);
            // How to check if execvp fails????
    
    default:
            // Parent Process
            // Background Process --- WNOHANG
            sleep(1); 
            if(*background_status == 1)
            {
              child_pid = waitpid(child_pid, &childStatus, WNOHANG);
              printf("Background: Parent(%d): Child(%d) terminated. Exiting\n", getpid(), child_pid);
              fflush(stdout);
            }
            // Foreground process
            else
            {
              child_pid = waitpid(child_pid, &childStatus, 0);
              printf("Foreground: Parent(%d): Child(%d) terminated. Exiting\n", getpid(), child_pid);
              fflush(stdout);
            }
            *exit_status = 0;
            return;
            }
  return;
  
  }

/*------------------------------------------------------------------------------------------*/
//  Change directory 
//    
//
/*------------------------------------------------------------------------------------------*/
void change_directory(char* new_path){

  if (new_path != NULL)
    {
      char path[256];
      strcpy(path, new_path);

      // Annex the \n
      size_t temp_len_path = strlen(path);
      path[temp_len_path - 1] = '\0';

      // Absolute Path
      if(strncmp(path, "~", 1) == 0)
      {
        // build the aboslute path name from HOME root
        char temp_buff[256];
        memset(&temp_buff, '\0', 256);
        char* root_dir = getenv("HOME");
        strcat(temp_buff, root_dir);
        strcat(temp_buff, &path[1]);

        if(chdir(temp_buff) == -1)
        {
          perror("error with cd/chdir absolute ");
          fflush(stdout);
        }
        // char temp_absolute[256];
        // getwd(temp_absolute);
        // printf("new cwd absolute: %s\n", temp_absolute);
      }

      // Relative path
      else if(chdir(path) == -1)
      {
        perror("error with cd/chdir relative ");
        fflush(stdout);
      }
      // char temp_relative[256];
      // getwd(temp_relative);
      // printf("New cwd relative %s\n", temp_relative);
    }

    // No second argument - change to directory specified in the HOME envvar
    else
    {
      chdir(getenv("HOME"));
      // char temp_noArg[256];
      // getwd(temp_noArg);
      // printf("new cwd no arg %s\n", temp_noArg);
    }
    return;
}
