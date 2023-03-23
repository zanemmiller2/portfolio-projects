; TITLE Project 6: String Primitives and Macros

; Author: Zane Miller
; Last Modified: 11/22/2021
; Description: This program implements two macros (mGetString and mDisplayString) for string 
;				processing and two procedures (ReadVal and WriteVal) for signed integers which use 
;				string primitive instructions. Finally, there is a test program in main which uses 
;				ReadVal and WriteVal to get 10 valid integers from the user, store these values in 
;				an array, display the integers, their sum and their average. 

INCLUDE Irvine32.inc

; ---------------------------------------------------------------------------------------------------------------------
; Name: mGetString
;
; Displays a prompt, gets the user's input into memory location of "VARIABLE_NAME", and provides a 
;		number of bytes read by the macro. 
;
; Preconditions: 
;		- Requires a count variable (bufferSize) for the length of the input string that can be accomodated
;			
; Receives:
;	- prompt = address of the userPrompt prompt message
;	- userInput = address of where the user string input will be stored
;	- userInputSize = maximum length of input string that can be accomodated by the macro
;	- bytesRead = address of where the size of the user input will be stored. 
;
; returns:
;	- userInput = address of the userInput string where the user input will be stored. 
;	- bytesRead = count of the number of bytes read by the macro from userInput
; ---------------------------------------------------------------------------------------------------------------------
mGetString	MACRO	prompt, userInput, userInputSize, bytesRead
	PUSH	EDX
	PUSH	ECX
	PUSH	EAX
	
	; Display initial prompt
	MOV		EDX, prompt
	CALL	WriteString
	; Get user input
	MOV		EDX, userInput
	MOV		ECX, userInputSize
	CALL	ReadString
	MOV		bytesRead, EAX

	POP		EAX
	POP		ECX
	POP		EDX
ENDM

; ---------------------------------------------------------------------------------------------------------------------
; Name: mDisplayString
;
; Prints the string which is stored in a specified memory location
;
; Preconditions:
;	- printStringAddr refers to the address OFFSET of the string to be printed. Passed to MACRO using BASE+OFFSET
;
; Receives:
;	- printStringAddr = address of string to be printed
; ---------------------------------------------------------------------------------------------------------------------
mDisplayString	MACRO	printStringAddr
	; Print the string passed by procedure
	MOV		EDX, printStringAddr
	CALL	WriteString 
ENDM


MAX_STRING_LENGTH_WSIGN = 11		; Max byte size of a 32 bit signed integer with sign
MAX_STRING_LENGTH  = 10				; Max byte size of a 32 bit signed integer without sign
MIN_STRING_LENGTH = 1				; Min byte size of a 32 bit signed integer without sign
MIN_STRING_LENGTH_WSIGN = 2			; Min byte size of a 32 bit signed integer with sign
USER_INPUT_LOOP_COUNTER = 10		; Sets the number of inputs the program will collect from the user. 

.data

programTitle			BYTE	"Project 6 - String Primitives and MACROs",13,10,0
programAuthor			BYTE	"Written by Zane Miller",13,10,0
userInstructionMsg1		BYTE	"Please provide 10 signed decimal integers.",13,10,0
userInstructionMsg2		BYTE	"Each number needs to be small enough to fit inside a 32-bit register.",13,10,0
userInstructionMsg3		BYTE	"After you have finished, I will display a list of the" 
						BYTE	"integers, their sum, and their average.",13,10,13,10,0
inputPrompt				BYTE	"Please enter a signed number: ",0
errorMsg				BYTE	"ERROR: You did not enter a signed number, or your number was too big.",13,10,0
tryAgainPrompt			BYTE	"Please try again: ",0
userInputNum			SDWORD	?
userInputStr			BYTE	33 DUP(?)
userInputBytesRead		DWORD	1 DUP(?)
userInputStrSize		DWORD	SIZEOF userInputStr
userInputArrayNum		SDWORD	10 DUP(?)
userInputArrayNumLen	DWORD	LENGTHOF userInputArrayNum
userInputArrayStr		DWORD	10 DUP(?)
runningSumNum			SDWORD	?
runningSumStr			BYTE	33 DUP(?)
runningSumMsg			BYTE	"The current running total is: ",0
userInputSumMsg			BYTE	"The sum of these numbers is: ",0
userInputRoundAvgNum	SDWORD	?
userInputRoundAvgStr	BYTE	33 DUP(?)
userInputRoundAvgMsg	BYTE	"The truncated average of these numbers is: ",0
lineNumberStr			BYTE	"00. ",0
displayArrayMsg			BYTE	"You entered the following numbers:",13,10,0
goodByeMsg				BYTE	"Thank you for playing!",13,10,0
nullString				BYTE	" ",0
commaSpaceStr			BYTE	", ",0
max32BitNumber			BYTE	"2147483647",0
max32BitNumberWSign		BYTE	"+2147483647",0
min32BitNumber			BYTE	"-2147483648",0
ecLineNumRunSum			BYTE	"**EC: Displays line number and running subtotal.",13,10,0

.code

main PROC

	; Display program title and author
	PUSH	OFFSET  ecLineNumRunSum
	PUSH	OFFSET	programAuthor
	PUSH	OFFSET	programTitle
	CALL	introduction

	; Display user instructions
	PUSH	OFFSET	userInstructionMsg3
	PUSH	OFFSET	userInstructionMsg2
	PUSH	OFFSET	userInstructionMsg1
	CALL	displayInstructions

;----------------------------------------------------------------------------------------
; This is the main loop body for collecting user inputs:
;	1. Initializes loop counter based on global USER_INPUT_LOOP_COUNTER.
;	2. Moves into ESI, the location of userNumArray used for storing the 
;		user input in an array. 
;	3. Sets a LOOP for collecting user input
;
; Within the LOOP:
;	1. Calls ReadVal to collect user input and convert string input to numerical value. 
;	2. Store the OFFSET of userInputNum in EDI and copy the numerical value to ESI 
;		(the location of the array used for storing a list of all user inputs).
;	3. LOOP through _getUserNumbersLoop until max entries have been received. 
;---------------------------------------------------------------------------------------
	MOV		ECX, USER_INPUT_LOOP_COUNTER
	MOV		ESI, OFFSET userInputArrayNum
	; Main user input collection loop
_getUserNumbersLoop:
	PUSH	OFFSET min32BitNumber				; OFFSET 64
	PUSH	OFFSET max32BitNumberWSign			; OFFSET 60
	PUSH	OFFSET max32BitNumber				; OFFSET 56
	PUSH	MIN_STRING_LENGTH_WSIGN				; OFFSET 52
	PUSH	MAX_STRING_LENGTH_WSIGN				; OFFSET 48
	PUSH	MIN_STRING_LENGTH					; OFFSET 44
	PUSH	MAX_STRING_LENGTH					; OFFSET 40
	PUSH	OFFSET lineNumberStr				; OFFSET 36
	PUSH	OFFSET userInputBytesRead			; OFFSET 32
	PUSH	OFFSET userInputNum					; OFFSET 28
	PUSH	userInputStrSize					; OFFSET 24
	PUSH	OFFSET userInputStr					; OFFSET 20
	PUSH	OFFSET tryAgainPrompt				; OFFSET 16
	PUSH	OFFSET errorMsg						; OFFSET 12
	PUSH	OFFSET inputPrompt					; OFFSET 8
	CALL	ReadVal
	; Store returned userInputNum value in userInputArrayNum
	MOV		EAX, userInputNum
	MOV		[ESI], EAX
	; Accumulate the running sum totaL
	ADD		runningSumNum, EAX
	; Display the running sum
	PUSH	OFFSET runningSumMsg
	PUSH	OFFSET runningSumStr
	PUSH	runningSumNum
	CALL	WriteVal
	; Increment userInputArrayNum index to store the next valid user input
	ADD		ESI, 4
	; Check if line number 9 has just printed. 

	LOOP	_getUserNumbersLoop
	JMP		_displayArrayInitialize

;-------------------------------------------------------------------------------------------------
; The following will: 
;	1. Display the array message "You entered the following numbers: "
;	2. Convert each element of the userInputArrayNum to a string
;	3. Display each element of the userInputArrayNum as a string separated by a comma and a space
;	4. Convert and display the total sum of the array of user inputs as a string
;	5. Calculate, convert and display the rounded average of the user inputs as a string. 
;-------------------------------------------------------------------------------------------------
_displayArrayInitialize:
	; Initialize EAX to 0 for indexing the userInputArrayNum
	MOV		EAX, 0
	; Set loop counter to length of userInputArrayNum
	MOV		ECX, LENGTHOF userInputArrayNum
	CALL	CrLf

	; Display array message
	CALL	CrLf
	mDisplayString OFFSET displayArrayMsg
_displayArrayLoop:
	; Copy element from userInputArrayNum to userInputNum
	MOV		EDI, userInputArrayNum[EAX]
	MOV		EBX, EDI
	MOV		userInputNum, EBX
	PUSH	OFFSET nullString					; OFFSET 16
	PUSH	OFFSET userInputStr					; OFFSET 12
	PUSH	userInputNum						; OFFSET 8
	; Convert and display indexed element of userInputArrayNum as string
	CALL	WriteVal
	; Increment EAX to point to next index in array
	ADD		EAX, 4
	CMP		ECX, 1
	JLE		_printNoCommaSpace
	; Comman, space separated values in array
	mDisplayString OFFSET commaSpaceStr
	LOOP	_displayArrayLoop
	CALL	CrLf

	; Does not print a comma and space after the last element of the array has been converted/printed
_printNoCommaSpace:
	LOOP	_displayArrayLoop
	CALL	CrLf

	; Converts and displays the total sum of the array
	CALL	CrLf
	PUSH	OFFSET	userInputSumMsg
	PUSH	OFFSET	runningSumStr
	PUSH	runningSumNum
	CALL	WriteVal
	CALL	CrLf

	; Calculate average from userInputArrayNum and stores in userInputRoundAvgNum
	CALL	CrLf
	PUSH	userInputArrayNumLen
	PUSH	OFFSET userInputRoundAvgNum
	PUSH	OFFSET runningSumNum
	CALL	calculateAverage

	; Converts and displays the rounded average of the array
	CALL	CrLf
	PUSH	OFFSET	userInputRoundAvgMsg
	PUSH	OFFSET	userInputRoundAvgStr
	PUSH	userInputRoundAvgNum
	CALL	WriteVal
	CALL	CrLf
	CALL	CrLf

	; Display farewell message
_goodbye:
	PUSH	OFFSET	goodByeMsg
	CALL	goodBye


	Invoke ExitProcess,0	; exit to operating system
main ENDP

; ------------------------------------------------------------------------------------------------
; Name: introduction
; 
; Displays the program title and author. 
;
; Receives:
;	- [EBP + 8] = address of programTitle string 
;	- [EBP + 12] = address of programAuthor string 
;	- [EBP + 16] = address of EC statement 1
;
; ------------------------------------------------------------------------------------------------
introduction	PROC
	PUSH	EBP
	MOV		EBP, ESP

	; Print the program title
	mDisplayString [EBP+8]
	; Print the program author
	mDisplayString [EBP+12]
	CALL	CrLf
	; Print EC statement 1
	mDisplayString [EBP+16]
	CALL	CrLf

	POP		EBP
	RET		12
introduction ENDP

; --------------------------------------------------------------------------------------------------------------------
; Name: displayInstructions
; 
; Displays the program instructions for the user. 
;
; Receives:
;	- [EBP + 8] = address of userInstructionMsg1 string 
;	- [EBP + 12] = address of userInstructionMsg2 string 
;	- [EBP + 16] = address of userInstructionMsg3 string 
;
; ---------------------------------------------------------------------------------------------------------------------
displayInstructions	PROC
	PUSH	EBP
	MOV		EBP, ESP

	; Display instruction line 1
	mDisplayString	[EBP+8]
	; Display instruction line 2
	mDisplayString	[EBP+12]
	; Display instruction line 3
	mDisplayString	[EBP+16]

	POP		EBP
	RET		12
displayInstructions ENDP

; ------------------------------------------------------------------------------------------------
; Name: ReadVaL
; 
; Description:
;	1. Defines and sets local constants for the minimum and maximum acceptable 
;		string values.
;	2. Prints line number and displays prompt and gets user input
;	3. Validates the user entered a valid length number, returns error and reprompts if invalid
;	4. Checks the sign of the number and updates signFlagLocal
;	5. Verifies that the user did not enter a value that exceeds the max and min value of a 32 bit register
;	6. Scans the userInput for unacceptable characters, returns error and reprompts if found. 
;	7. Converts the string input to numerical value and stores in userInputNum
;
; Postconditions: 
;	- userInputBytesRead will store the number of bytes the user input to validate user entered a number thats at
;		least within the bounds of max/min acceptable length.
;
; Receives: 
;	- [EBP+8]  = address of inputPrompt
;	- [EBP+12] = address of errorMsg
;	- [EBP+16] = address of tryAgainPrompt
;	- [EBP+20] = address of userInputStr used for collecting user input
;	- [EBP+24] = userInputStrSize used for bufferSize in mGetString MACRO
;	- [EBP+28] = address of userInputNum used for storing the user input as a numerical value after conversion from ascii
;	- [EBP+32] = userInputBytesRead used for comparing the size of the user input size to the min/max allowable bytes
;	- [EBP+36] = address of lineNumberStr
;	- [EBP+40] = address of MAX_STRING_LENGTH
;	- [EBP+44] = address of MIN_STRING_LENGTH
;	- [EBP+48] = address of MAX_STRING_LENGTH_WSIGN
;	- [EBP+52] = address of MIN_STRING_LENGTH_WSIGN
;	- [EBP+56] = address of max32BitNumber
;	- [EBP+60] = address of max32BitNumberWSign
;	- [EBP+64] = address of min32BitNumber
;	
; Returns: 
;	- userInputNum = number converted string from validated userInput.
; ------------------------------------------------------------------------------------------------
ReadVal	PROC
	
	LOCAL	signFlagLocal:SDWORD
	LOCAL	stringSumLocal:SDWORD
	LOCAL	stringDigitLocal:SDWORD

	PUSH	EAX
	PUSH	ESI
	PUSH	ECX
	PUSH	EBX
	PUSH	EDI

;---------------------------------------------------------------------------------
; This section does the following:
;	1. Increments the line counter and adjusts for line 10
;	2. Displays the prompt and collects the user input and stores in [EBP+20]
;	3. Initial check of the first character of the user input (+, -, or num 0-9)
;	4. Compares the length of the user input
;		- Greater than 11 bytes with a sign (or 10 without sign) 
;		  results in invalid input error
;		- Less than 2 bytes with a sign (or 1 byte without sign)
;		  results in invalid input error
;	5. Compares the "value" of the user input with local Globals 
;	   (MAX_32BIT_NUMBER, MAX_32BIT_NUMBER_WSIGN, MIN_32BIT_NUMBER)
;		- If user string is greater than the glabal string an invalid input 
;			error is printed
;---------------------------------------------------------------------------------	
	CALL	CrLf
	; Checks if line 09. has been printed and increments line number or writes line 10
	MOV		EDI, [EBP+36]
	ADD		EDI, 1
	MOV		EDX, [EDI]
	CMP		EDX, 2108985
	JGE		_lineNumberTen
	ADD		EDX, 1
	MOV		[EDI], EDX

_getInput:
	mDisplayString [EBP+36]
	mGetString [EBP+8], [EBP+20], [EBP+24], [EBP+32]
	JMP		_checkFirstCharacter

	; Writes 1 to the first element of lineNumberStr and writes 0 to the second element
_lineNumberTen:
	MOV		EDI, [EBP+36]
	MOV		EDX, 49
	MOV		[EDI], EDX
	ADD		EDI, 1
	MOV		EDX, 48
	MOV		[EDI], EDX
	ADD		EDI, 1
	MOV		EDX, 46
	MOV		[EDI], EDX
	ADD		EDI, 1
	MOV		EDX, 32
	MOV		[EDI], EDX
	JMP		_getInput
	
	; Checks that the first character is either "+", "-", or num in range [0,9]
_checkFirstCharacter:
	MOV		ESI, [EBP+20]
	LODSB
	MOV		signFlagLocal, 1
	CMP		AL, 43					
	JE		_compareLengthWithSign				
	MOV		signFlagLocal, -1
	CMP		AL, 45
	JE		_compareLengthWithSign
	MOV		signFlagLocal, 1
	CMP		AL, 48
	JL		_invalidInput
	CMP		AL, 57
	JG		_invalidInput
	JMP		_compareLengthWithoutSign

	; Verifies user input is <= 11 bytes and >= 2 bytes
_compareLengthWithSign:
	MOV		ECX, [EBP+32]
	CMP		ECX, [EBP+52]			; MIN_STRING_LENGTH_WSIGN
	JL		_invalidInput
	CMP		ECX, [EBP+48]			; MAX_STRING_LENGTH_WSIGN
	JG		_invalidInput
	JL		_initializeScanStringLoopWithSign
	; Input is exactly 11 bytes
	JMP		_getSign

_getSign:
	MOV		ESI, [EBP+20]
	LODSB	
	MOV		ECX, [EBP+48]			; MAX_STRING_LENGTH_WSIGN
	MOV		ESI, [EBP+20]
	MOV		EDI, [EBP+60]			; max32BitNumberWSign
	CMP		AL, 43
	JE		_compareMaxValueWithSign
	MOV		EDI, [EBP+64]			; min32BitNumber
	CMP		AL, 45
	JE		_compareMinValue

	; Verifies user input is <= 10 bytes and >= 1 bytes
_compareLengthWithoutSign:
	MOV		ESI, [EBP+20]
	MOV		EDI, [EBP+56]			; max32BitNumber
	MOV		ECX, [EBP+32]
	CMP		ECX, [EBP+40]			; MAX_STRING_LENGTH
	JG		_invalidInput
	JE		_compareMaxValueWithoutSign
	CMP		ECX, [EBP+44]			; MIN_STRING_LENGTH
	JL		_invalidInput
	JMP		_initializeScanStringLoopNoSign

	; Verifies user did not enter a number less than "-2147483648"
_compareMinValue:
	CMPSB
	JG		_invalidInput
	LOOP	_compareMinValue
	MOV		signFlagLocal, -1
	JMP		_initializeScanStringLoopWithSign

	; Verifies user did not enter a number greater than "+2147483647"
_compareMaxValueWithSign:
	CMPSB
	JG		_invalidInput
	LOOP	_compareMaxValueWithSign
	MOV		signFlagLocal, 1
	JMP		_initializeScanStringLoopWithSign

	; Verifies user did not enter a number greater than "2147483647"
_compareMaxValueWithoutSign:
	CMPSB
	JG		_invalidInput
	LOOP	_compareMaxValueWithoutSign
	MOV		signFlagLocal, 1
	JMP		_initializeScanStringLoopNoSign

; ------------------------------------------------------------------------
;	_invalidInput:
;		1. clears the userInputStr
;		2. Resets the stringSumLocal and stringDigitLocal to 0
;		3. Reinvokes mGetString and jumps back to _validateLength
; ------------------------------------------------------------------------
_invalidInput:
	; Clears userInputStr when user enters an invalid number
	MOV		EDI, [EBP+20]
	XOR		EAX, EAX
	MOV		ECX, [EBP+32]
	CLD
	REP		STOSB
	; Resets stringSumLocal and stringDigitLocal to 0 for string to numerical conversions
	MOV		stringSumLocal, 0
	MOV		stringDigitLocal, 0
	; Displays error message
	mDisplayString [EBP+12]
	; Resets userInputBytesRead to 0
	MOV		EDI, [EBP+32]
	MOV		EAX, 0
	MOV		EDI, EAX
	; Invokes mGetString with tryAgainPrompt to recollect user input
	mgetString	[EBP+16], [EBP+20], [EBP+24], [EBP+32]
	JMP		_checkFirstCharacter

; -------------------------------------------------------------------
; Initializes a loop counter depending on whether a leading sign 
;	was enthered or not. If a sign was entered, the loop conter is 
;	decremented by one and comparison starts with the second character. 
;	
;	If the character is a valid number, the character is converted to 
;	an absolute value integer and stored in LOCAL stringSum. If the 
;	number is negative, it is converted at the end. 
; -------------------------------------------------------------------
_initializeScanStringLoopWithSign:
	; Initialize the stringSumLocal used for converting from ascii to numerical
	MOV		stringSumLocal, 0
	MOV		stringDigitLocal, 0
	; Sets Loop counter equal to 1 less than the byteCount to account for the first element "+"/"-"
	MOV		ECX, [EBP+32]
	SUB		ECX, 1
	MOV		ESI, [EBP+20]
	; Begins checking first character after sign
	ADD		ESI, 1
	JMP		_scanStringLoop

_initializeScanStringLoopNoSign:
	; Sets loop counter equal to byteCount since first element is not "+"/"-"
	MOV		stringSumLocal, 0
	MOV		stringDigitLocal, 0
	MOV		ECX, [EBP+32]
	MOV		ESI, [EBP+20]
	JMP		_scanStringLoop

_scanStringLoop:
	; Searches the userInputString for any non-numerical characters other than "+"/"-" in first element
	MOV		EAX, 0
	LODSB
	; Checks user input ascii value not less than "0"
	CMP		AL, 48
	JL		_invalidInput
	; Checks user input ascii value not greater than "9"
	CMP		AL, 57
	JG		_invalidInput
	
	CMP		signFlagLocal, 1
	JE		_convertPositiveNumber
	JMP		_convertNegativeNumber

; -----------------------------------------------------------------------------
; Converts the string character to a number [10*stringSum + (stringSum - 48)]
;	1. Subtracts 48 from the ascii character and moves it to LOCAL stringDigit
;	2. Moves stringSum to EAX and multiplies it by 10
;	3. Adds the current stringDigit (AL - 48) and stringSum and stores in stringSum
;	4. Loops to scan the next string character. 
;	5. When loop breaks:
;		1. Check if user string was negative.
;			- If yes, convert to NEG and continue, otherwise continue to 
;			  _writeUserInputNum 
;		2. Write string to memory at userInputNum
; -----------------------------------------------------------------------------	
_convertPositiveNumber:
	; Convert number to integer representation, becomes the current stringDigitLocal
	SUB		AL, 48
	MOV		stringDigitLocal, EAX
	; Moves the current sum to EAX and multiplies by 10
	MOV		EAX, stringSumLocal
	MOV		EBX, 10
	MUL		EBX
	; Adds the current digit to the end of the current number, and saves updated stringSumLocal
	ADD		EAX, stringDigitLocal
	MOV		stringSumLocal, EAX
	LOOP	_scanStringLoop
	; If the number is positive, write it to memeory
	CMP		signFlagLocal, 1
	JE		_writeUserInputNum
	; If the number is negative, convert to negative, then write to memory
	MOV		EAX, stringSumLocal
	NEG		EAX
	MOV		stringSumLocal, EAX
	JMP		_writeUserInputNum

_convertNegativeNumber:
	; Convert number to integer representation, becomes the current stringDigitLocal
	SUB		AL, 48
	NEG		EAX
	MOV		stringDigitLocal, EAX
	; Moves the current sum to EAX and multiplies by 10
	MOV		EAX, stringSumLocal
	MOV		EBX, 10
	IMUL	EBX
	; Adds the current digit to the end of the current number, and saves updated stringSumLocal
	ADD		EAX, stringDigitLocal
	MOV		stringSumLocal, EAX
	LOOP	_scanStringLoop
	; If the number is positive, write it to memeory
	CMP		signFlagLocal, 1
	JE		_writeUserInputNum
	; If the number is negative, convert to negative, then write to memory
	MOV		EAX, stringSumLocal
	JMP		_writeUserInputNum

_writeUserInputNum:
	; Writes the converted uuserInputStr to memory location of userInputNum
	MOV		EAX, stringSumLocal
	MOV		ESI, [EBP+28]
	MOV		[ESI], EAX
	JMP		_endProc

_endProc:
	POP		EDI
	POP		EBX
	POP		ECX
	POP		ESI
	POP		EAX
	RET		60
ReadVal ENDP

; ------------------------------------------------------------------------------------------------
; Name: calcualteAverage
; 
; Calculates the average of the userInputArray
;
; Preconditions: 
;	- userInputArrayNum is a 10 element array of SDWORD integer values
;
; Receives: 
;	- [EBP+8] = address of runningSumNum
;	- [EBP+12] = address of userInputRoundAvgNum for storing the calculated rounded average
;	- [EBP+16] = address of userInputArrayLen used for dividing sum of the elements
;
; Returns: 
;	- userInputRoundAvgNum = rounded average of all the integers in the userInputArray
; ------------------------------------------------------------------------------------------------
calculateAverage	PROC
	PUSH	EBP
	MOV		EBP, ESP
	PUSH	EDI
	PUSH	ESI
	PUSH	EAX
	PUSH	EBX

	; Move the sum into EAX
	MOV		EDI, [EBP+8]

	; Move the total number of elements into EBX for division and compute average
	MOV		EBX, [EBP+16]
	MOV		EAX, [EDI]
	CDQ
	IDIV	EBX

	; Copy the calculated rounded average to userInputRoundAvgNum
	MOV		EDI, [EBP+12]
	MOV		[EDI], EAX

	POP		EBX
	POP		EAX
	POP		ESI
	POP		EDI
	POP		EBP
	RET		12
calculateAverage	ENDP

; --------------------------------------------------------------------------------------------------------------------
; Name: WriteVal
; 
;	Displays:
;		1. The message of what is being displayed (running sum, array, sum, average...)
;	For each array, sum, and average:
;		1. Displays the appropriate description string. 
;		2. Converts the appropriate array, sum or average integer to a string
;		3. Invokes mDisplayString to display the appropriate array, sum, or average as a string. 
;
;	Preconditions:
;		- array elements, sum and average must be represented as a SDWORD integer value to convert to string
;
; Receives: 
;	- [EBP+8]  = address of number to be converted to string
;	- [EBP+12] = address of string data label to store string of converted numerical value
;	- [EBP+16] = address of message to display
;
; Returns: 
;	- userInputRoundAvgStr = string representation of the rounded user average
;	- runningSumStr = string representation of the userInputArray sum
;	- userInputStr = string representation of each element of the userInputArray for printing. 
;
;--------------------------------------------------------------------------------------------------------------------
WriteVal PROC
	LOCAL	digitCounterLocal:DWORD		; used for keeping track of the number of digits in integer
	LOCAL	signFlagLocal:SDWORD		; used for keeping track of sign of integer

	PUSH	EDX
	PUSH	EAX
	PUSH	EBX
	PUSH	ESI
	PUSH	EDI
	PUSH	ECX

	; display message of what will be shown, array, sum, avg...
	mDisplayString [EBP+16]

	; Clear the string representation for the next number
	MOV		EDI, [EBP+12]		
	XOR		EAX, EAX
	MOV		ECX, 11
	CLD
	REP		STOSB

;-------------------------------------------------------------------------------------------
;	The following block converts a signed integer to a string by:
;		1. initializes the conversionLoop
;			- Moves numerical value to ESI
;			- Moves address of string variable to EDI
;			- Moves the number to EAX to determine if it is positive or negative
;			- Sets the divisor to 10
;		2. Checking whether the number is "-2147483648", pos, or negative.
;			- "-2147483648" 
;			- Positives will prepends a "+" on its string and set signFlag = 1
;			- Negatives will prepend a "-" on its string and set signFlag = -1.
;		3. Converts the absolute value of the integer number to its individual components.
;			- Convert to absVal by multiplying by signFlag
;			- Divide resulting quotient by 10 until quotient == 0
;			- Push remainders to stack
;			- When qotient == 0 jump to appendStrLoop
;		4. Append the string by:
;			- Popping remainders from stack.
;			- Adding 48 to integer to get ASCII representation.
;			- Store byte at EDI.
;			- Displaying string by appropriate variant.
;-------------------------------------------------------------------------------------------
	; Initialize conversion loop
	MOV		digitCounterLocal, 0
	MOV		ESI, [EBP+8]		; numerical representation
	MOV		EDI, [EBP+12]		; string representation
	MOV		EAX, ESI
	MOV		EBX, 10
	; Checks if the user entered exactly "-2147483648"
	CMP		EAX, 80000000h		; Hex = -2147483648
	JE		_convertMin32BitNumber
	CMP		EAX, 0
	JL		_convertNegativeNumber
	JGE		_convertPositiveNumber

_convertMin32BitNumber:
	; Prepend "-" on desitnation string and set signFlagLocal to -1
	MOV		BYTE PTR [EDI], 45
	MOV		signFlagLocal, -1
	INC		EDI
	JMP		_divisionLoop32BitMin

_convertNegativeNumber:
	; Prepend "-" on desitnation string and set signFlagLocal to -1
	MOV		BYTE PTR [EDI], 45
	MOV		signFlagLocal, -1
	INC		EDI
	; Gets the absolute val of the user input to conver to string
	IMUL	signFlagLocal
	JMP		_divisionLoopNeg

_convertPositiveNumber:
	; Prepend "+" on desitnation string and set signFlagLocal to 1
	MOV		BYTE PTR [EDI], 43		
	MOV		signFlagLocal, 1
	INC		EDI
	JMP		_divisionLoopPos

;-------------------------------------------------------------------------------------------
; The division loop converts each integer into its individual string components by: 
;	1. Clears the high remainder EDX 
;	2. Divides EAX by 10
;	3. Pushes the remainder to the stack
;	4. Increments the digitCounterLocal to keep track of how many digits are in the converted number
;	5. Compares the quotient to 0:
;		- If quotient is 0, we have divided the last digit and can exit the loop
;		- Otherwise continue dividing by 10 until we have separated each digit
;	6. Sets the appendStrLoop counter equal to the number of digits in number
;	7. Move to concatenating the remainders as a single string
;-------------------------------------------------------------------------------------------
_divisionLoopNeg:
	CDQ
	IDIV	EBX						; =10 set above _convertMin32BitNumber
	PUSH	EDX						
	INC		digitCounterLocal
	CMP		EAX, 0
	JNE		_divisionLoopNeg
	MOV		ECX, digitCounterLocal
	JMP		_appendStrLoopNeg

_divisionLoopPos:
	CDQ
	IDIV	EBX						; =10 set above _convertMin32BitNumber
	PUSH	EDX						
	INC		digitCounterLocal
	CMP		EAX, 0
	JNE		_divisionLoopPos
	MOV		ECX, digitCounterLocal
	JMP		_appendStrLoopPos

;-----------------------------------------------------------------------
; -2147483648 is a pain in the ass. It does something weird because its
;   hex value is weird. So I had to negate the remainder before pushing
;	to the stack for reasons I'm not 100% sure about. 
;-----------------------------------------------------------------------
_divisionLoop32BitMin:
	CDQ
	IDIV	EBX						; =10 set above _convertMin32BitNumber
	NEG		EDX
	PUSH	EDX						
	INC		digitCounterLocal
	CMP		EAX, 0
	JNE		_divisionLoop32BitMin
	MOV		ECX, digitCounterLocal
	JMP		_appendStrLoop32BitMin

;-------------------------------------------------------------------------------------------
; appendStrLoop:
;	1. Pops the last remainder into EAX
;	2. Adds 48 to EAX to convert numeral to ascii code
;	3. Stores the string value at address pointed to by EDI 
;		(string representation of numerical variable)
;	4. Jumps to displaying the string representation of the number by invoking mDisplayString
;-------------------------------------------------------------------------------------------
_appendStrLoopPos:
	POP		EAX
	ADD		AL, 48
	STOSB	
	LOOP	_appendStrLoopPos
	JMP		_displayNumString

_appendStrLoopNeg:
	POP		EAX
	ADD		AL, 48
	STOSB	
	LOOP	_appendStrLoopNeg
	JMP		_displayNumString

	; Technically not needed but I'm keeping it because I'm iritated with -2147483648.
	; And it makes debugging easier.
_appendStrLoop32BitMin:
	POP		EAX
	ADD		AL, 48
	STOSB	
	LOOP	_appendStrLoop32BitMin
	JMP		_displayNumString
	

_displayNumString:
	; displays the number as a string
	mDisplayString [EBP+12]

	POP		ECX
	POP		EDI
	POP		ESI
	POP		EBX
	POP		EAX
	POP		EDX
	RET		12
WriteVal ENDP

; ---------------------------------------------------------------------------------------------------------------------
; Name: goodBye
; 
; Displays the farewell message
;
; Receives:
;	- [EBP + 8] = address of goodByeMsg string
; ---------------------------------------------------------------------------------------------------------------------
goodBye	PROC
	PUSH	EBP
	MOV		EBP, ESP

	; Display farwell message
	CALL	CrLf
	mDisplayString	[EBP+8]

	POP		EBP
	RET		4
goodBye	ENDP



END main
