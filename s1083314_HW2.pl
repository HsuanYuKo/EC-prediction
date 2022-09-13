#!/usr/bin/perl -w
use strict;

#mkdir train test
my $trainfn = shift; # argument
my @train = split />/, `cat $trainfn`;
my $testfn = shift; # argument
my @test = split />/, `cat $testfn`;

sub p{
  my $get; #train 100，test 20
  my @myfile; #train,test
  my $savefile; #存進去的資料夾名
  my $labelfile;
  
  ($get, $savefile,$labelfile ,@myfile)= @_;
  my @countEC = (0, 0, 0, 0, 0, 0);
  
  for (my $i = 1;$i < (scalar(@myfile));$i = $i+1)
  {
    #find EC num
    $myfile[$i] = '>' . $myfile[$i]; #把>補回來
    my $EC;
    my $beforeEC;
    $myfile[$i] =~ />(\S+):(\d+)./ and ($beforeEC, $EC) = ($1, $2);
    
    if ($countEC[$EC] >= $get){ #看那種EC有沒有超過100/20了
      next;
    }
    
    open(DATA, ">", "$savefile/$beforeEC.fasta") or die "$beforeEC.fasta檔案無法開啟, $!"; #建檔
    print DATA $myfile[$i]; #寫檔
    close(DATA);
    
    `bin/psiblast -db uniprot.fasta -query $savefile/$beforeEC.fasta -out outfile -outfmt 6 -save_pssm_after_last_round -out_ascii_pssm "$savefile/$beforeEC.pssm"`;
    
    my @pssm = split /\n/, `cat "$savefile/$beforeEC.pssm"`;
    my $head = index($pssm[2], "A") - 1;
    my $end = index($pssm[2], "V");
    my $long = $end - $head + 1;
    splice(@pssm, 0, 3); #刪前面
    splice(@pssm, scalar(@pssm)-6, 7); #刪後面
    for (my $j = 0;$j < (scalar(@pssm));$j = $j+1){
      $pssm[$j] = substr($pssm[$j], $head, $long);
      $pssm[$j] = $pssm[$j]."\n";
    }
    #print (@pssm);
      
    if (scalar(@pssm) >= 100) #ROW超過100再存前100列並存起來
    {
      print($beforeEC,":",$EC);
      print("\n");
      $countEC[$EC] = $countEC[$EC] + 1;

      @pssm = @pssm[0..99]; #拿前100條
      open(FH,'>',"$savefile/$beforeEC.pssm") or die "檔案無法開啟, $!";
      print FH @pssm;
      close(FH);
      
      open(FH,'>',"$labelfile/$beforeEC.txt") or die "檔案無法開啟, $!";
      print FH $EC;
      close(FH);
      }
    else
    {
      `rm -f "$savefile/$beforeEC.pssm"`;
    }
    `rm -f "$savefile/$beforeEC.fasta"`;
  }
}

if(!(-e "/train")){
   `mkdir train`;
 }
if(!(-e "/test")){
   `mkdir test`;
 }
#if(!(-e "/cnntrain")){
#   `mkdir cnntrain`;
# }
#if(!(-e "/cnntest")){
#   `mkdir cnntest`;
# }
if(!(-e "/labeltrain")){
   `mkdir labeltrain`;
 }
if(!(-e "/labeltest")){
   `mkdir labeltest`;
 }
&p(100, "train", "labeltrain", @train);
&p(20, "test", "labeltest",@test);

#my $R = `Rscript s1083314_HW2.r`;
my $pythonfile = `python3.7 s1083314_HW2.py`;
