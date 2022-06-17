#include <sys/wait.h> // for waitpid

#include <fcntl.h>    // for open,
#include <stdio.h>    // for printf and perror
#include <stdlib.h>   // for exit
#include <unistd.h>   // for execv, getpid, fork
#include <string.h>   // for string operations (strtok)

#define MAXARGS 512   // first argument is command
#define MAXSTRING 2048
#define MAXFILELEN 256

void get_cl_input(char*[], char in_file_name[], char out_file_name[]);
void change_directory(char* new_path);
void execute_command(char*[], char in_file_name[], char out_file_name[], struct sigaction, struct sigaction);


volatile sig_atomic_t foreground_only_mode = 0; // allow background
void sigtstp_handler(int signo)
{
  if(foreground_only_mode == 0) // background is allowed
  {
    char* sigtstp_message = "Entering foreground-only mode (& is now ignored)\n"; // 49 char
    write(STDOUT_FILENO, sigtstp_message, 50);
    foreground_only_mode = 1; // switch to true - dont allow background
  }
  else
  {
    char* sigtstp_message_exit = "Exiting foreground-only mode\n"; // 29 char
    write(STDOUT_FILENO, sigtstp_message_exit, 30);
    foreground_only_mode = 0; // change back to false -- allow background
   }
}

int childStatus = -44;
int zombie_counter = 0;         // Counts the number of background processes waiting to be reaped
int zombies[20];                // Array to store the pids of background processes not yet reaped
int background_stat = 0;        // 0 - process is not background; 1 - process is background (&) present
int exit_stat = 0;              // Variable to store the exit status of a process


int main()
{
  char* user_input[MAXARGS];        // array of 512 pointers - max number of args
  char in_file_name[MAXFILELEN];    // max path name length = 256
  char out_file_name[MAXFILELEN];   // max file name length = 256
   
  
  // From module on Signal Handling API -- SIGINT
  struct sigaction SIGINT_action = {0};
  SIGINT_action.sa_handler = SIG_IGN;       // Parent process ignores SIGINT
  sigfillset(&SIGINT_action.sa_mask);
  SIGINT_action.sa_flags = 0;
  sigaction(SIGINT, &SIGINT_action, NULL);
  
  // Modeled after code from module on Signal Handling API -- SIGSTP
  struct sigaction SIGTSTP_action = {0};
  SIGTSTP_action.sa_handler = sigtstp_handler;      // Parent process will invoke sigtstp_handler to switch between foreground_only_mode
  sigfillset(&SIGTSTP_action.sa_mask);
  SIGTSTP_action.sa_flags = 0;
  sigaction(SIGTSTP, &SIGTSTP_action, NULL); 
  
  // Loops infinitely until user enters "exit" command
  while(1)
  {
      // Reap background processes that have terminated by iterating through list of zombies[]
    for(int i = 0; i < zombie_counter; i++)
    {
        if(waitpid(zombies[i], &childStatus, WNOHANG) > 0)
        {
            // process exited by signal
          if(WIFSIGNALED(childStatus))
          {
            printf("Pid %d terminated by signal %d\n", zombies[i], WTERMSIG(childStatus));
            fflush(stdout);
          }
            // Process exited by status
          else if(WIFEXITED(childStatus))
          {
            printf("background pid %d is done exit value %d\n", zombies[i], WEXITSTATUS(childStatus));
            fflush(stdout);  
          }
          zombie_counter--;
        }
      }

    // Sanitize the arrays -- point pointers in arguments array to 0 before collecting user input
    for(int i = 0; i < MAXARGS; i++)
    {
      user_input[i] = NULL;
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
    fflush(stdout);
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
          // builtins ignore &
        background_stat = 0;
        // chdir unsuccessful
        if(chdir(getenv("HOME")) == -1)
        {
          perror("cd");
          fflush(stdout);
        }
      }
      // Got to relative/absolute path
      else
      {
          // absolute path relative to user's HOME
        if(user_input[1][0] == '~')
        {
            // Get user's HOME directory from environmental variables
          char* rootpath = getenv("HOME");
          char temp_path[256];              // array to build absolute path relative to user's HOME
          memset(&temp_path, '\0', 256);    // Clean the array first -- remove extraneous junk values
          strcat(temp_path, rootpath);      // Copy the rootpath to temp_path
          strcat(temp_path, &user_input[1][1]); // Append the user's input to rootpath

          if(chdir(temp_path) == -1)
          {
              // chdir failed -- absolute path
            perror("cd");
            fflush(stdout);
          }
        }
        else if (chdir(user_input[1]) == -1)
        {
            // chdir failed -- relative path
          perror("cd");
          fflush(stdout);
        }
      }
    } 

    /* Status */
    // if this command is run before any foreground command simply return exit status 0
    // 3 builtins don't count as foreground processes for the purposes of this status
    else if(strncmp(&user_input[0][0], "status\0", 7) == 0)
    {
      printf("error value %d\n", exit_stat);
      background_stat = 0;
    }

    /* Non Built-Ins */
    else
    {
      execute_command(user_input, in_file_name, out_file_name, SIGINT_action, SIGTSTP_action);
    }

    // Sanitize the arrays for next command -- its here and at the beginning -- cause C cannot be trusted
    for(int i = 0; user_input[i]; i++)
    {
      user_input[i] = NULL;
    }
  }
}

/*------------------------------------------------------------------------------------------*/
//  Get/Parse user input from command line
//      - User input is stored in a temp_input array before tokenizing input commands, arguments, input/output files
//      - $$ expansion is taken care of by 1st checking if the token contains the string '$$' and then expanding the '$$' to PID
//      - returns when token's return NULL
/*------------------------------------------------------------------------------------------*/
void get_cl_input(char* get_input[], char in_file_name[], char out_file_name[]){
  // temp array for getting input from stdin
  char temp_input[2048];    // max input length as specified
  char* token;              // stores the tokenized input
  char* strdup();           // allocates sufficient memory for copy
  
  // get input from command line (stdin)
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
  
  // switch \n to \0 at end of input
  if(temp_input[temp_index - 1] == '\n')
  {
    // replace \n with \0
    temp_input[temp_index - 1] = '\0';
  }

  // check for background mode -- last input is & and background mode is allowed
  if(temp_input[temp_index - 2] == '&' && foreground_only_mode == 0)
  {
    background_stat = 1;        // update the background status to True (1)
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
      // next token after < is in_file name
      token = strtok(NULL, " ");
      strcpy(in_file_name, token);
    }

    // output redirection
    else if(strcmp(token, ">") == 0)
    {
      // next token after > is out_file name
      token = strtok(NULL, " ");
      strcpy(out_file_name, token);
    }

    // background process  
    else if(strcmp(token, "&") == 0)
    {
        // process can run in background -- i.e & is last character
        if(background_stat == 1)
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
        }

        // & is at end but not allowed to run in background
        else if(foreground_only_mode == 1)
        {
          continue;
        }

        // & is not at end -- part of string
        else
        {
            get_input[i] = token;
        }
    }

    // commands + [args...]
    else 
    {
      /* -------------- Handle $$ expansion ----------- */
      // '$$' exists in token
      if(strstr(token, "$$"))
      {
        char temp_orig[256];        // copy of token
        char temp_build[256];       // new string to append to
        char temp_pidStr[8];        // pid_max on a 64 bit system ~2^22 (7 digits);
        int orig_index = 0;         // trailing counter
        int build_index = 0;        // forward counter
        int pid_index = 0;          // pid string counter
        
        strcpy(temp_orig, token);   // make a copy of the token
        
        // Convert pid to string
        snprintf(temp_pidStr, 7, "%d", getpid());

        while(orig_index <= strlen(temp_orig))
        {
            // found consecutive '$'
          if(temp_orig[orig_index] == '$' && temp_orig[orig_index + 1] == '$')
          {
            // copy over pid char
            for(int p = 0; temp_pidStr[p]; p++)
            {
              temp_build[build_index] = temp_pidStr[pid_index];
              build_index++;
              pid_index++;
            }
            // reset the pid index
            pid_index = 0;
            orig_index = orig_index + 2;    // skip counter forward to past the $$
          }

          // copy over regular char
          else
          {
            temp_build[build_index] = temp_orig[orig_index];
            build_index++;
            orig_index++;
          }
        }
        // copy new string to get_input
        get_input[i] = strdup(temp_build);
      }
      /*--------------------------------------------------------------------------------------*/
      
      // No $$ in string
      else
      {
        // - strdup allocates sufficent memory for the copy
        get_input[i] = strdup(token);
      }
    }
    // get next token
    token = strtok(NULL, " ");
  }
  return;
}

/*------------------------------------------------------------------------------------------*/
//  Execute commands not built in
//    
//
/*------------------------------------------------------------------------------------------*/
void execute_command(char* user_input[], char in_file_name[], char out_file_name[], struct sigaction SIGINT_action, struct sigaction SIGTSTP_action){
  
  int input_fd, new_in_fd, output_fd, new_out_fd;
  
  // fork a new process
  pid_t child_pid = fork();
  switch(child_pid)
  {
    case -1:
            // fork error
            perror("fork()\n");
            fflush(stdout);
            exit(1);

    case 0:
            // child process ignores SIGINT
          SIGINT_action.sa_handler = SIG_IGN;
          sigaction(SIGINT, &SIGINT_action, NULL);

          /* --- Handle input/output redirection --- */
          // get the file desriptor of the input_file (input redirected)
          if (strncmp(&in_file_name[0], "\0", 1) != 0)
          {
            input_fd = open(in_file_name, O_RDONLY, 00600);

            // file input error
            if(input_fd == -1)
            {
              perror("Error");
              fflush(stdout);
                
              // Set exit status but dont exit shell -- just exit child
              exit_stat = 1;
              exit(exit_stat);         
            }

            // update with stdin file descriptor
            int result = dup2(input_fd, 0);

            // test reassignment unsuccessful -- set exit status to 1
            if(result == -1)
            {
              perror("in error at dup");
              fflush(stdout);
              exit_stat = 1;
              exit(exit_stat);
            }
          }
          // get the file descriptor of the output_file (output redirected)
          if(strncmp(&out_file_name[0], "\0", 1) != 0)
          {
            output_fd = open(out_file_name, O_WRONLY | O_CREAT | O_TRUNC, 0600);

            // file open error
            if(output_fd == -1)
            {
              perror("Error");
              fflush(stdout);
              // Set exit status but dont exit shell
              exit_stat = 1;
              exit(exit_stat);
            }

            // update stdout file descriptor -- dup2 returns the new fd
            int result = dup2(output_fd, 1);

            // test reassignment unsuccessful
            if(result == -1)
            {
              perror("out error at dup");
              fflush(stdout);
              exit_stat = 1;
              exit(exit_stat);            
            }
          }

          // error if execvp fails -- execvp only returns on error
          if(execvp(user_input[0], user_input) == -1){
            perror("execvp");
            exit_stat = 1;
            exit(exit_stat);
          }

    default:
            // Parent Process
            // Background Process --- WNOHANG
            if(background_stat == 1 && foreground_only_mode == 0)
            {
              printf("background pid is %d\n", child_pid);
              fflush(stdout);
              zombies[zombie_counter] = child_pid;
              zombie_counter++;
              child_pid = waitpid(child_pid, &childStatus, WNOHANG);
              background_stat = 0;
            }

            // Foreground process
            else
            {
              child_pid = waitpid(child_pid, &childStatus, 0);
              // Check child's exit status/signal
              if(WIFSIGNALED(childStatus))
              {
                exit_stat = WTERMSIG(childStatus);  
              }
              else if(WIFEXITED(childStatus))
              {
                exit_stat = WEXITSTATUS(childStatus);
              }
            }
            break;
  }
}