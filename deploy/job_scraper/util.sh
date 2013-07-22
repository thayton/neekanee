#
# Install software updates
#
function system_update {
    apt-get update
    apt-get -y install aptitude
    aptitude -y full-upgrade
}

# system_add_user(username, password, groups, shell=/bin/bash)
function system_add_user {
    USERNAME=`lower $1`
    PASSWORD=$2
    SUDO_GROUP=$3
    SHELL=$4

    if [ -z "$4" ]; then
        SHELL="/bin/bash"
    fi

    useradd --create-home --shell "$SHELL" --user-group --groups "$SUDO_GROUP" "$USERNAME"

    echo "$USERNAME:$PASSWORD" | chpasswd
}

# system_sshd_edit_bool (param_name, "Yes"|"No")
# eg, system_sshd_edit_bool "PermitRootLogin" "no"
function system_sshd_edit_bool {
    VALUE=`lower $2`
    if [ "$VALUE" == "yes" ] || [ "$VALUE" == "no" ]; then
        sed -i "s/^#*\($1\).*/\1 $VALUE/" /etc/ssh/sshd_config
    fi
}
 
function system_sshd_permitrootlogin {
    system_sshd_edit_bool "PermitRootLogin" "$1"
}

# see https://help.ubuntu.com/community/UFW
function system_security_ufw_configure_basic {
    ufw logging on
    ufw default deny

    ufw allow ssh/tcp
    ufw limit ssh/tcp
 
    ufw allow http/tcp
    ufw allow https/tcp
 
    ufw enable
}

function mysql_install {
    # $1 - the mysql root password
 
    if [ ! -n "$1" ]; then
        echo "mysql_install() requires the root pass as its first argument"
        return 1;
    fi
 
    echo "mysql-server-5.1 mysql-server/root_password password $1" | debconf-set-selections
    echo "mysql-server-5.1 mysql-server/root_password_again password $1" | debconf-set-selections
    apt-get -y install libmysqlclient-dev # for mysql_config 
    apt-get -y install mysql-server mysql-client

    echo "Sleeping while MySQL starts up for the first time..."
    sleep 5
}
 
function mysql_tune {
    # Tunes MySQL's memory usage to utilize the percentage of memory you specify, defaulting to 40%
 
    # $1 - the percent of system memory to allocate towards MySQL
 
    if [ ! -n "$1" ];
        then PERCENT=40
        else PERCENT="$1"
    fi
 
    sed -i -e 's/^#skip-innodb/skip-innodb/' /etc/mysql/my.cnf # disable innodb - saves about 100M
 
    MEM=$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo) # how much memory in MB this system has
    MYMEM=$((MEM*PERCENT/100)) # how much memory we'd like to tune mysql with
    MYMEMCHUNKS=$((MYMEM/4)) # how many 4MB chunks we have to play with
 
    # mysql config options we want to set to the percentages in the second list, respectively
    OPTLIST=(key_buffer sort_buffer_size read_buffer_size read_rnd_buffer_size myisam_sort_buffer_size query_cache_size)
    DISTLIST=(75 1 1 1 5 15)
 
    for opt in ${OPTLIST[@]}; do
        sed -i -e "/\[mysqld\]/,/\[.*\]/s/^$opt/#$opt/" /etc/mysql/my.cnf
    done
 
    for i in ${!OPTLIST[*]}; do
        val=$(echo | awk "{print int((${DISTLIST[$i]} * $MYMEMCHUNKS/100))*4}")
        if [ $val -lt 4 ]
            then val=4
        fi
        config="${config}\n${OPTLIST[$i]} = ${val}M"
    done
 
    sed -i -e "s/\(\[mysqld\]\)/\1\n$config\n/" /etc/mysql/my.cnf
    touch /tmp/restart-mysql
}

function mysql_create_database {
    # $1 - the mysql root password
    # $2 - the db name to create
 
    if [ ! -n "$1" ]; then
        echo "mysql_create_database() requires the root pass as its first argument"
        return 1;
    fi

    if [ ! -n "$2" ]; then
        echo "mysql_create_database() requires the name of the database as the second argument"
        return 1;
    fi
 
    echo "CREATE DATABASE $2 CHARACTER SET utf8;" | mysql -u root -p$1
}
