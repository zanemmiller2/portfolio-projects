#include <sys/wait.h> // for waitpid
#include <sys/types.h>
#include <fcntl.h>    // for open,
#include <stdio.h>    // for printf and perror
#include <stdlib.h>   // for exit
#include <unistd.h>   // for execv, getpid, fork
#include <string.h>   // for string operations (strtok)
#include <stdbool.h>  // for background bool value
#include <setjmp.h>
#define MAXARGS 512   // first argument is command
#define MAXSTRING 2048
#define MAXFILELEN 256

void get_cl_input(char*[], char in_file_name[], char out_file_name[]);
void change_directory(char* new_path);
void execute_command(char*[], char in_file_name[], char out_file_name[], struct sigaction);
// void sigchld_catcher(int signo);

/* -------------------------- Signal catcher for background children ------------------------------------------- */
// SIGCHLD has no default action so there is no need to pass to child.
/*void sigchld_catcher(int signo){
  pid_t caught_kid_pid;
  int status;
  caught_kid_pid = waitpid(-1, &status, WNOHANG);
  if(caught_kid_pid > 0){

    if 
    printf("background pid %d is done: exit value %d\n", caught_kid_pid, status);
    }

  }
*/

int childStatus = -5;
int zombie_counter = 0;
int zombies[20];
int background_stat = 0;
int exit_stat = 0;

int main()
{
  char* user_input[MAXARGS];      // array of 512 pointers - max number of args
  char in_file_name[MAXFILELEN];     // max path name length = 256
  char out_file_name[MAXFILELEN];    // max file name length = 256
  int pid = getpid();
   
  int i = 0;
  // with c99 std initializing the first one NULL works. gnu99 works with the first two.
  user_input[0] = NULL;
  user_input[1] = NULL;
  while(user_input[i])
  {
    user_input[i] = NULL;
    i++;
  }

  // From module on Signal Handling API -- SIGINT
  struct sigaction SIGINT_action = {0};
  SIGINT_action.sa_handler = SIG_IGN;
  sigfillset(&SIGINT_action.sa_mask);
  SIGINT_action.sa_flags = 0;
  sigaction(SIGINT, &SIGINT_action, NULL);

  /*// SIGCHLD -- used for tracking background processes
  struct sigaction SIGCHLD_action = {0};
  SIGCHLD_action.sa_handler = sigchld_catcher;
  sigfillset(&SIGINT_action.sa_mask);
  SIGCHLD_action.sa_flags = 0;
  sigaction(SIGCHLD, &SIGCHLD_action, NULL);*/

  while(1)
  {
    for(int i = 0; i < zombie_counter; i++)
    {
        if(waitpid(zombies[i], &childStatus, WNOHANG) > 0)
        {
          if(WIFSIGNALED(childStatus))
          {
            printf("Termination by signal %d\n", WTERMSIG(childStatus));
            fflush(stdout);
          }
          else if(WIFEXITED(childStatus))
          {
            printf("background pid %d is done exit value %d\n", zombies[i], WEXITSTATUS(childStatus));
            fflush(stdout);  
          }
          zombie_counter--;
        }
      }

    // clean out input and output file names
    for (int i = 0; i < strlen(in_file_name); i++)
    {
      in_file_name[i] = '\0';
    }
    for (int i = 0; i < strlen(out_file_name); i++)
    {
      out_file_name[i] = '\0';
    }

    
    // prompt
    printf(": ");
    fflush(stdout);

    // Go get user input from stdin - will return here
    get_cl_input(user_input, in_file_name, out_file_name);

    // Check for comments and empty lines
    if((user_input[0][0] == '#') || (user_input[0][0] == '\0'))
    {
      /* ----- THOU SHALT NOT PASS ... empty commands and comments  ------- */
    }


    /* ----- Built ins ----- */

    /* Exit */
    else if(strncmp(&user_input[0][0], "exit\0", 5) == 0)
    {
      background_stat = 0;
      for(int i = 0; i < zombie_counter; i++)
      {
        kill(zombies[zombie_counter], SIGKILL);
      }
      exit(0);
    }

    /* cd */
    else if(strncmp(&user_input[0][0], "cd\0", 3) == 0)
    {
      // User did not enter destination argument - cd to $HOME
      if(!user_input[1])
      {
        background_stat = 0;
        chdir(getenv("HOME"));
      }
      // Got to relative/absolute path
      else
      {
        background_stat = 0;
        chdir(user_input[1]);
      }
    } 

    /* Status */
    // if this command is run before any foreground command simply return exit status 0
    // 3 builtins dont count as foreground processes for the purposes of this status
    else if(strncmp(&user_input[0][0], "status\0", 7) == 0)
    { 
      background_stat = 0;
      printf("error value %d\n", exit_stat);
      exit_stat = 0;
    }

    /* Non Built-Ins */
    else
    {
      execute_command(user_input, in_file_name, out_file_name, SIGINT_action);
      
    }

    // reset the arrays for next command 
    for(int i = 0; user_input[i]; i++)
    {
      user_input[i] = NULL;
    }
  }
}

/*------------------------------------------------------------------------------------------*/
//  Get/Parse user input from command line 
//    
//
/*------------------------------------------------------------------------------------------*/
void get_cl_input(char* get_input[], char in_file_name[], char out_file_name[]){
  // temp array for getting input from stdin
  char temp_input[2048];    // max input length as specified
  char* token;
  char* strdup();           // allocates sufficient memory for copy
  
  // get input
  fgets(temp_input, 2048, stdin);

  // strip out new line char + replace with \0 -- this just makes my life a little easier. 
  int temp_index = strlen(temp_input);

  // better take care of the blank line input here before shit depends on an initialized array
  if(temp_index == 1)
  {
    // copy a space into get_input for checking to ignore later
    get_input[0] = strdup("\0");
    return;
  }

  if(temp_input[temp_index - 1] == '\n')
  {
    // replace \n with \0
    temp_input[temp_index - 1] = '\0';
  }

  // get the first token
  token = strtok(temp_input, " ");
  for (int i = 0; i < temp_index; i++)
  {
    if(!token)
    {
      return; //no more tokens :(
    }

    // input redirection
    else if(strcmp(token, "<") == 0)
    {
      // next token is in_file name
      token = strtok(NULL, " ");
      strcpy(in_file_name, token);
    }

    // output redirection
    else if(strcmp(token, ">") == 0)
    {
      // next token is out_file name
      token = strtok(NULL, " ");
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
      // set background status to True
      background_stat = 1;
    }

    // commands + [args...]
    else 
    {
      /* -------------- Handle $$ expansion (as of now assuming only 2 chars at end) ----------- */
      if(strstr(token, "$$"))
      {
        char temp_orig[256];  // copy of token
        char temp_build[256]; // new string to append to
        char temp_pidStr[8]; // pid_max on a 64 bit system ~2^22 (7 digits); 
        int orig_index = 0;
        int build_index = 0;
        int pid_index = 0;
        
        strcpy(temp_orig, token);
        
        // Convert pid to string
        snprintf(temp_pidStr, 8, "%d", getpid());

        while(orig_index < strlen(temp_orig))
        {
          if(temp_orig[orig_index] == '$' && temp_orig[orig_index + 1] == '$')
          {
            // copy over pid char
            for(int p = 0; temp_pidStr[p]; p++)
            {
              temp_build[build_index] = temp_pidStr[pid_index];
              build_index++;
              pid_index++;
            }
            pid_index = 0;
            orig_index = orig_index + 2;
          }

          // copy over regular char
          else
          {
            temp_build[build_index] = temp_orig[orig_index];
            build_index++;
            orig_index++;
          }
        }
        get_input[i] = strdup(temp_build);
      }
      /*--------------------------------------------------------------------------------------*/
      
      // No $$ in string
      else
      {
        // - strdup allocates sufficent memory for the copy
        get_input[i] = strdup(token);
      }
      // printf("Command entered: %s\n", get_input[i]);
      // fflush(stdout);
    }
    token = strtok(NULL, " ");
  }
  return;
}

/*------------------------------------------------------------------------------------------*/
//  Execute commands not built in
//    
//
/*------------------------------------------------------------------------------------------*/
void execute_command(char* user_input[], char in_file_name[], char out_file_name[], struct sigaction SIGINT_action){
  
  int* childStatus; 
  int input_fd, new_in_fd, output_fd, new_out_fd;
  
  // fork a new process
  pid_t child_pid = fork();
  switch(child_pid)
  {
    case -1: 
            perror("fork()\n");
            fflush(stdout);
            exit_stat = 1;
            exit(1);

    case 0:
          //printf("Child(%d) running %s command\n", getpid(), user_input[0]);
          // fflush(stdout);

          SIGINT_action.sa_handler = SIG_IGN;
          sigaction(SIGINT, &SIGINT_action, NULL);

          /* --- Handle input/output redirection --- */
          // get the file desriptor of the input_file (input redirected)
          if (strncmp(&in_file_name[0], "\0", 1) != 0)
          {
            //printf("In name: %s\n", in_file_name);
            //fflush(stdout);
            input_fd = open(in_file_name, O_RDONLY, 00600);

            // file input error
            if(input_fd == -1)
            {
              perror("Error");
              fflush(stdout);
                
              // Set exit status but dont exit shell -- just exit child
              exit_stat = 1;
              exit(1);         
            }

            // update with stdin file descriptor
            int result = dup2(input_fd, 0);

            // test reassignment unsuccessful
            if(result == -1)
            {
              perror("in error at dup");
              fflush(stdout);
              exit_stat = 1;
              exit(1);
            }
          }
          // get the file desriptor of the output_file (output redirected)
          if(strncmp(&out_file_name[0], "\0", 1) != 0)
          {
            //printf("Out name: %s\n", out_file_name);
            //fflush(stdout);
            output_fd = open(out_file_name, O_WRONLY | O_CREAT | O_TRUNC, 00600);

            // file open error
            if(output_fd == -1)
            {
              printf("open() failed on \"%s\"\n", out_file_name);
              fflush(stdout);
              perror("Error");
              fflush(stdout);
              // Set exit status but dont exit shell
              exit_stat = 1;
              exit(1);
            }

            // update stdout file descriptor -- dup2 returns the new fd
            int result = dup2(output_fd, 1);
            // test reassignment successful
            if(result == -1)
            {
              perror("out error at dup");
              fflush(stdout);
              exit_stat = 1;
              exit(1);            
            }
          }
          
          if(execvp(user_input[0], user_input) == -1){
            perror("execvp");
            exit_stat = 1;
            exit(1);
          }

    default:
            // Parent Process
            // Background Process --- WNOHANG
            if(background_stat == 1)
            {
              printf("background pid is %d\n", child_pid); 
              zombies[zombie_counter] = child_pid;
              zombie_counter++;
              fflush(stdout);
              child_pid = waitpid(child_pid, childStatus, WNOHANG);
              background_stat = 0;
                            
            }
            // Foreground process
            else
            {
              child_pid = waitpid(child_pid, childStatus, 0);
              //printf("Foreground: Parent(%d): Child(%d) terminated. Exiting\n", getpid(), child_pid);
              //fflush(stdout);
            }
            return;
            }
  return;
}





/*------------------------------------------------------------------------------------------*/
//  Change directory -- dont think i need this 
//    
//
/*------------------------------------------------------------------------------------------*/
/*void change_directory(char* new_path){

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
}*/
