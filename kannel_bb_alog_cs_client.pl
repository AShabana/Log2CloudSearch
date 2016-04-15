#!/usr/bin/perl
use Data::UUID ;
#use threads ('yield',
              #'stack_size' => 64*4096,
              #'exit' => 'threads_only',
              #'stringify');
use threads ;

        #
# #---------'1->date              $3->smsc         $4->ACT       $5->FID     $6->from       $7->to               $8->msg_txt
$Pat = '((.+? ){2}).*?\[SMSC\:(.*?)\] .*?\[ACT\:(.*?)\] .*?\[FID\:(.*?)\] .*?\[from\:(.*?)\] \[to\:(.*?)\] .*?\[msg\:\d+\:(.*?)\].*' ;
$threshold = 19;
$count = 0 ;
$json_line = "" ;
$uuid_gen = Data::UUID->new ;
$output_file_name = "output.json.";
$ext_oscillator = 0 ;
$output_file = "" ;
$uuid = "";

sub cloudsearch_uploader {
        # take file and upload it
        $cmd = "aws cloudsearchdomain  --endpoint-url http://doc-kanneljs-wfvp6oqir5lp7mqhcwmiichulq.us-east-1.cloudsearch.amazonaws.com upload-documents --content-type application/json --documents  $output_file ";
        print "$cmd \n";
        system $cmd;
        system ">  $output_file";
        $count=0;
        #sleep 10 ;
}

sub init_ofile {
        $ext_oscillator++;
        $output_file_ext = $ext_oscillator%3;
        $output_file = $output_file_name . $output_file_ext ;
        open(OUTPUT, ">>" . $output_file);
        print OUTPUT $json_line . "\n";
        $count++ ;
}

sub ofile_done {
        close OUTPUT;
        #threads->create( cloudsearch_uploader) ;
        cloudsearch_uploader();
        $count=0;
}

sub ofile_add_json{
   $line = @_[0] ;
   $uuid = @_[1] ;
   $type = @_[2] ;
   #print "line -> $line \ntype -> $type \n" ;
   if ( $line =~ m/$Pat/ ){
        $json = "" ;
        if ( $type == 'sms' ){
                $json = "{\"fields\":{\"time\":\"$1\",\"message_type\":\"Sent SMS\",\"sender\":\"$6\",\"receipent\":\"$7\",\"message\":\"$8\",\"smsc\":\"$3\",\"account_name\":\"$4\"},\"id\":\"$uuid\",\"type\":\"add\"}" ;
        }elsif( $type == 'dlr'){
                $json = "{\"fields\":{\"time\":\"$1\",\"message_type\":\"Receive DLR\",\"sender\":\"$6\",\"receipent\":\"$7\",\"message\":\"$8\",\"smsc\":\"$3\",\"account_name\":\"$4\"},\"id\":\"$uuid\",\"type\":\"add\"}" ;
        }else{
                print "Strange not sms nor unkown !!!!!!\n" ;
                print '\t(' . $line . ')\n'
                #return -1 ;
        }
        if ($count == 0){
                $json_line = "[" . $json. "," ;
                init_ofile() ;
        } elsif ($count < $threshold){
                $json_line = $json . "," ;
                print OUTPUT $json_line . "\n";
                $count++ ;
        }elsif ($count == $threshold){
                $json_line = $json . "]\n" ;
                print OUTPUT $json_line . "\n";
                ofile_done() ;
        }
   }
}

# This the main()
while (<STDIN>)
{
        my $line = $_ ;
        if ( $DEBUG) { print "$line \n"; }
        $uuid =  $uuid_gen->create_str();
        if ( substr( $line, 20, 11 ) eq 'Receive DLR') { #/* Receive DLR*/
                ofile_add_json($line, $uuid, 'dlr') ;
        }else{
                ofile_add_json($line, 'sms');
        }
}

print $json_line = "{}]" ;
print OUTPUT $json_line . "\n" ;
#threads->create( cloudsearch_uploader, $output_file ) ;
close OUTPUT;
cloudsearch_uploader() ;
