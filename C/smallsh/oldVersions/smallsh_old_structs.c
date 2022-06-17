#include <sys/wait.h> // for waitpid
#include <sys/types.h>
#include <fcntl.h>    // for open,
#include <stdio.h>    // for printf and perror
#include <stdlib.h>   // for exit
#include <unistd.h>   // for execv, getpid, fork
#include <string.h>   // for string operations (strtok)
#include <stdbool.h>  // for background bool value
#define MAXARGS 511   // first argument is command
#define MAXSTRING 2048
#define MAXFILELEN 256
// structure of user_input parsed
typedef struct input_command{
  char* cmd;
  int* numArgs;
  char* args[512];
  char input_file[256];
  char output_file[256];
  int background;
} input_struct;

void get_user_input (input_struct *user_input);
void change_directory(input_struct * user_input);
void execute(input_struct *user_input, int* exit_stat);
  /* ----------------------------------------------------------------- */
  /* ---------------------------- Main ------------------------------- */
  /* ----------------------------------------------------------------- */

int main(void){
  struct input_command user_input;

  int* exit_stat;
  int exit_status = 0;
  exit_stat = &exit_status;
  // Initialize the strucutre variables
  // user_input.cmd[256];        // Sizes will change
  user_input.numArgs = 0;
  // user_input.input_file[256];  // Sizes will change
  // user_input.output_file[256]; // Sizes will change
  user_input.background = 0;

    // int child status


// signal strucutre to handle ^C --- SIG_INT
   // Your shell, i.e., the parent process, must ignore SIGINT
   // Any children running as background processes must ignore SIGINT
   // A child running as a foreground process must terminate itself when it receives SIGINT
   // The parent must not attempt to terminate the foreground child process; instead the foreground child (if any) must terminate itself on receipt of this signal.
   // If a child foreground process is killed by a signal,
      // the parent must immediately print out the number of the signal that killed it's foreground child process (see the example) before prompting the user for the next command.

// signal structure to handle ^Z --- SIG_STOP
    // A child, if any, running as a foreground process must ignore SIGTSTP.
    // Any children running as background process must ignore SIGTSTP.
    // When the parent process running the shell receives SIGTSTP
        // The shell must display an informative message (see below) immediately if it's sitting at the prompt,
        // or immediately after any currently running foreground process has terminated
        // The shell then enters a state where subsequent commands can no longer be run in the background.
        // In this state, the & operator should simply be ignored, i.e., all such commands are run as if they were foreground processes.
    // If the user sends SIGTSTP again, then your shell will
        // Display another informative message (see below) immediately after any currently running foreground process terminates
        // The shell then returns back to the normal condition where the & operator is once again honored for subsequent commands, allowing them to be executed in the background.
        // See the example below (IN ASSINGMENT PDF) for usage and the exact syntax which you must use for these two


  // while user input is not "exit"
  do
  {
    memset(user_input.cmd, '\0', 256);
    memset(user_input.input_file, '\0', 256);
    memset(user_input.output_file, '\0', 256);
    user_input.background = 0;
    user_input.numArgs = 0;

    printf("~: ");
    fflush(stdout);
    /* ----- Get/Parse User Input ----- */
    get_user_input(&user_input);

    // ------------------------------- Test prints -------------------------------------------
    // printf("%s\n", user_input.cmd);    // print cmd
    // printf("Number of args %d\n", *user_input.numArgs); // print number of args
    // for(int i = 0; i < *user_input.numArgs; i++){         // print args
    //   printf("Arg[%d]: %s\n", i, user_input.args[i]);
    // }
    // printf("Length of inputfile: %lu\n", strlen(user_input.input_file));
    // if(strcmp(user_input.input_file, "")){            // print input files
    //   printf("input file - %s\n", user_input.input_file);
    // }
    // printf("Length of output file: %lu\n", strlen(user_input.output_file));
    // if(strcmp(user_input.output_file, "")){           // pint output files
    //   printf("output file - %s\n", user_input.output_file);
    // }
    // printf("Background Value: %d\n", *user_input.background);
    // printf("parent pid: %lu %d\n", sizeof(getpid()), getpid());
    // char cwd[256];
    // getwd(cwd);
    // printf("previous wd: %s\n", cwd);
    // ------------------------------------------------------------------------------------------


    /* ------------------------------- Execute ------------------------------- */


    /* ----- Ignore Commands ----- */

    // if first argument in "input" is "#" or ""
    if(user_input.cmd[0] == '#' || user_input.cmd[0] == '\0'){
      continue;
      }

    /* ----- Handle $$ expansion ---- */

    // the command has at least 1 set of $$
    if(strstr(user_input.cmd, "$$") != 0)
    {
      // temp string holder for pid#
      char* temp_pidStr[10];

      // Convert pid to string
      snprintf(temp_pidStr[0], 10, "%d", getpid());
      // get the length of the pid
      int len_tempPid = strlen(*temp_pidStr);
      // Allocates memory for the temp_cmd = len of command + len of the pid + 1 null terminating string
      char temp_cmd[256];

      size_t i = 0;                // temp_cmd counter
      int user_input_index = 0; // user_input.cmd counter

      // Clear the temp_cmd before writing to it
      memset(temp_cmd, '\0', strlen(user_input.cmd));
      while(i < (strlen(user_input.cmd) + len_tempPid + 1))
      {
        // There is a '$$' - append the pid to temp_cmd
        if(user_input.cmd[user_input_index] == '$' && user_input.cmd[user_input_index+1] == '$')
        {
          temp_cmd[i] = '\0';

          // Concatenate pid
          snprintf(&temp_cmd[i], len_tempPid+1, "%d", getpid());

          // skip temp to end of pid
          i = i + len_tempPid;

          // skip user_input.cmd past 2nd $
          user_input_index = user_input_index + 2;
        }

        // No $$ yet -- just copy 1 char from user_input.cmd to temp
        else
        {
          temp_cmd[i] = user_input.cmd[user_input_index];
          i++;
          user_input_index++;
        }
      }

      // copy the temp back to user_input.cmd
      strcpy(user_input.cmd, temp_cmd);
      
    }

    // test print
    // printf("%s\n", user_input.cmd);
    // fflush(stdout);


    /* ----- Built ins ----- */

    // ---------------------- Handle "EXIT" ---------------------- //
    if (strncmp(user_input.cmd, "exit", 4) == 0)
    {
      // Kill all processes???

      // Free memory allocation
      // free(user_input.cmd);
      // free(user_input.input_file);
      // free(user_input.output_file);

      // Call exit
      exit(0);
    }


    // ---------------------- Handle "CD" ---------------------- //
    else if(strncmp(user_input.cmd, "cd", 2) == 0)
    {
      change_directory(&user_input);
      continue;
    }

    // ---------------------- Handle "STATUS" ---------------------- //
    // if status is run before any foreground command - simply return exit status 0 ???
    else if(strncmp(user_input.cmd, "status", 6) == 0)
    {
      // exited by signal
      if(WIFSIGNALED(*exit_stat))
      {
        // print out process status/signal
        printf("Abnormal termination by signal  %d\n", WTERMSIG(*exit_stat));
        fflush(stdout);
      }

      // exited by status
      else
      {
        // print out process status/signal
        printf("Termination by status %d", WEXITSTATUS(*exit_stat));
        fflush(stdout);
      }
      continue;
    }

    /* ---------------------- Handle "NON-BUILT INS ELSE" ---------------------- */
    // background status handing when parsing input string and stored as user_inpuut.background
    else
    {
      execute(&user_input, exit_stat);
    }
  }
  while(1);
}

/* --------------------------------------------------------------------------------------------------------------------*/
//                  #################  Get user input #################
//
//    char* user_input_comand  ---input array for storing parsed user command
//    int* background  --- bool value of background/foreground status
//
//    Locals
//     - user_input_string[2048] --- local string array for storing user input. Will be parsed to user_input_command
/* --------------------------------------------------------------------------------------------------------------------*/
void get_user_input (input_struct *user_input){ //int* background, pid?, input_file, output_file)

  char user_input_string[MAXSTRING];   // local input string for getting user command from stdin
  char* token;                         // Token for parsing command line


  /* ----- Get Input String ----- */

  // fgets returns a pointer to user_input_string
  fgets(user_input_string, MAXSTRING, stdin);

  // strip off the "\n" chararcter
  user_input_string[strlen(user_input_string) - 1] = '\0';
  // printf("%s\n", user_input_string);
  // printf("%p\n", user_input->cmd);


    /* ----- Parse Input String ----- */
    // separate input string by space loop until new line is found?  --- feed to input structrure
    // strtok with " " delimiter or** fscanf

    // get the command
    token = strtok(user_input_string, " ");
    user_input->cmd = token;


    int argIndex = 0;
    int backgroundVal = 0;
    // get everyting after the command
    for(int i = 0; i < MAXARGS; i++){
      token = strtok(NULL, " ");

      // Token is Null or
      if(!token){
        user_input->background = backgroundVal;
        user_input->numArgs = &argIndex;
        return;
      }

      // Token is < - tokenize again and store as user_input->input_file
      else if(strcmp(token, "<") == 0){
        token = strtok(NULL, " ");
        memset(&user_input->input_file, '\0', 20);
        strcpy(user_input->input_file, token);
      }

      // Token is > - tokenize again and store as user_input->output_file
      else if(strcmp(token, ">") == 0){
        token = strtok(NULL, " ");
        memset(&user_input->output_file, '\0', 20);
        strcpy(user_input->output_file, token);
      }

      // Token is & - update background value
      else if(strcmp(token, "&") == 0){
        strcpy(user_input->input_file, "/dev/null");
        strcpy(user_input->output_file, "/dev/null");
        printf("Setting background to True.\n");
        fflush(stdout);
        backgroundVal = 1;
      }

      // Token is [args...]
      else{
        user_input->args[argIndex] = malloc(strlen(token) + 1);
        user_input->args[argIndex] = token;
        argIndex++;
      }
    }
    return;
}
  /* ----------------------------------------------------------------- */
  /* ------------------------ Execute Command ------------------------ */
  /* ----------------------------------------------------------------- */
void execute(input_struct *user_input, int* exit_stat){

  int childStatus;
  int input;
  int output;
  char* command = calloc(20, 1);
  command = user_input->cmd;




  // fork
  pid_t child_pid = -5;
  child_pid = fork();

  switch(child_pid)
  {
    // fork fail
    case -1:
      perror("fork()\n");
      fflush(stdout);
      *exit_stat = 1;
      exit(1);

    // Child process
    case 0:
      // printf("Child(%d) running %s command\n", getpid(), command);
      // fflush(stdout);

      // Handle input/output redirection

      // get the file desriptor of the input_file (input redirected)
      if (*user_input->input_file == NULL)
      {
        input = open(user_input->input_file, O_RDONLY);
        // file open error
        if(input == -1)
        {
          printf("open() failed on \"%s\"\n", user_input->input_file);
          perror("Error");
          fflush(stdout);
          // Set exit status but dont exit shell
          *exit_stat = 1;
          exit(1);          // break???
        }
        // update stdin file descriptor
        if(dup2(input, 0) == -1)
        {
          perror("in fail");
          perror("error at dup");
        }
        fcntl(input, F_SETFD, FD_CLOEXEC);
      }

      // get the file desriptor of the output_file (output redirected)
      if (user_input->output_file == NULL)
      {
        output = open(user_input->output_file, O_WRONLY);
        // file open error
        if(output == -1)
        {
          printf("open() failed on \"%s\"\n", user_input->input_file);
          perror("Error");
          fflush(stdout);
          // Set exit status but dont exit shell
          *exit_stat = 1;
          exit(1);          // break???
        }

        // update stdout file descriptor
        if(dup2(output, 1) == -1)
        {
          printf("out fail\n");
          perror("error at dup");
        }
        fcntl(output, F_SETFD, FD_CLOEXEC);
      }

      char args[512];
      strcpy(args, *user_input->args);
      execlp(command, command, args, NULL);

      perror("execlp");
      exit(1);



    default:
      // execute in background
      if(user_input->background == 1)
      {
        // printf("parent(%d), waiting for child(%d) background\n", getpid(), child_pid);
        child_pid = waitpid(child_pid, &childStatus, WNOHANG);
        // printf("finished background\n");
        fflush(stdout);
        break;
      }
      else
      {
        // printf("parent(%d), waiting for child(%d) foreground\n", getpid(), child_pid);
        child_pid = waitpid(child_pid, &childStatus, 0);
        // printf("finished foreground\n");
        // fflush(stdout);
        break;
      }
      }
  // free(command);
  return;
}

            /* ------ Child ------ */
            // case 0 - child process execute

              /* --- Inout/Output Redirection --- */
              // input/output redirection
                // dup2() --- using stdin_fileno and stdout_fileno ??
                  // if it is a background command and:
                    // if no input redirection for background command --- redirect stdin to /dev/null
                    // if no output redirection for background command --- redirect stdout to /dev/null

                // if input_redirrection via stdin fails to open() read only
                  // print error
                  // set exit status to 1
                  // dont exit shell

                // if output_redirrection via stdout fails to open() write only
                  // print error
                  // set exit status to 1
                  // dont exit shell

                /* --- execvp --- */
                // If execvp fails ---
                  // Indicate command doest exist
                  // set value retrieved by status to 1
                  // terminate process

                // terminate if receive SIG_INT as foreground  --- separate function sig_stat handle function???? or handle self???
                // Ignore SIG_STOP --- separate function sigstat handle function???? or handle self???

                // if background process
                  // ignore SIG_INT + SIG_STOP --- separate function sigstat handle function???? or handle self???
                  // print process id of background when it begins

                // after child executes --- terminate whether success or failure

            /* ------ Parent ------ */
            // default
              // wait if background == false
                // print signal number that killed child process if child terminated because of SIGINT or handle self???
              // wait WNOHANG if bacground == true


      // when background process terminates --- print process id and exit status before next prompt shows
      // CLEAR VARIABLES
      // RETURN TO MAIN **PROMPT AGAIN**




/* ---------- Get/Set Process Status / Signal ---------- */
// void get_status_signal(pid)
  // sig_int
  // sig_stop
  // Dont use printf for SIGINT and SIGSTP


/* --------------------------------------------------------------------------------------------------------------
#   Function changes the cwd based on the built-in cd command. Handles reltive and absolute paths. If no path
#   specified, directory changes to path specified in the HOME environment variable
#   Receives:
#     - input_struct * user_input   ---- Accesses user_input.args[0] to determine the path if present
#   Returns:
#     - none
#
---------------------------------------------------------------------------------------------------------------*/
void change_directory(input_struct *user_input){

  if (*user_input->numArgs > 0)
    {
      char* path = user_input->args[0];

      // Absolute Path
      if(path[0] == '~')
      {
        char temp_buff[256];
        char* root_dir = getenv("HOME");
        memset(temp_buff, '\0', 256);
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
      char temp_noArg[256];
      chdir(getenv("HOME"));
      memset(temp_noArg, '\0', 256);
      // getwd(temp_noArg);
      // printf("new cwd no arg %s\n", temp_noArg);
    }
    return;
}