# Function to switch JDK versions
function setjdk() {
    echo "Select the java version you wish to switch to from the following:" 
    echo 
    options=()
    count=-1

        while IFS= read -r line
        do
            if [[ ! "$line" == M* ]] && [[ ! "$line" == /* ]] && [[ ! -z "$line" ]]; then
                options+=("$line")
                ((count++))
                echo '['"$count"']'${options["$count"]}
            fi
        done < <(/usr/libexec/java_home -V 2>&1)

    echo 
    read -p "Please chose a value from the options above: " selectedOption </dev/tty
    
    if [ "$count" -ge "$selectedOption" ] && [ "$selectedOption" -ge '0' ]; then
        removeFromPath '/System/Library/Frameworks/JavaVM.framework/Home/bin'
        removeFromPath "$JAVA_HOME/bin"
        stringArray=(${options["$selectedOption"]})
        export JAVA_HOME="${stringArray[@]: -1}"
        export PATH="$JAVA_HOME"/bin:$PATH
        echo "JAVA_HOME is set to be ${JAVA_HOME}"
    else
        echo "Invalid option, JAVA_HOME was not set"
    fi
}

function removeFromPath() {
  export PATH=$(echo $PATH | sed -E -e "s;:$1;;" -e "s;$1:?;;")
 }
