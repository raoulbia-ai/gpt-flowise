//returns todays date

/*
* You can use any libraries imported in Flowise
* You can use properties specified in Input Schema as variables. Ex: Property = userid, Variable = $userid
* You can get default flow config: $flow.sessionId, $flow.chatId, $flow.chatflowId, $flow.input
* You can get custom variables: $vars.<variable-name>
* Must return a string value at the end of function
*/

  function getTodaysDate() {
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      
      const formattedDate = `${year}-${month}-${day}`;
      return formattedDate;
  }

  try {
      const todayDate = getTodaysDate();
      return(todayDate);
  } catch (error) {
      console.error("Error getting today's date:", error);
      return '';
  }
