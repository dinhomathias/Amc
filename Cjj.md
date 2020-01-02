/*
BY     : @php88
CH① : @TALKMANY
لا تنشر بدون حقوق
*/


$update = json_decode(file_get_contents('php://input'));
$message = $update->message;
$chat_id = $message->chat->id;
$text = $message->text;
$id = $message->from->id;
// المتغيرات اللازمة //
$API_KEY = '823866847:AAEDqUrqbvf15Byhisy03RyY2yP5PZ_I2hg '
$get = file_get_contents("https://api.telegram.org/bot$API_KEY/getChatMember?chat_id=$chat_id&user_id=".$id);
$info = json_decode($get, true);
$homsi = $info['result']['status'];
$admin = ; 1008990777
$getChatMembersCount = "http://api.telegram.org/bot".API_KEY."/getChatMembersCount?chat_id=$chat_id";
$file_get = file_get_contents($getChatMembersCount);
$json = json_decode($file_get);
$member = $json->result;
$bot_tele1 = file_get_contents("bot_tele1.txt");

if ( $id == $admin ){
if (preg_match("10 .*/", $text) ) {
    $bot_tele1 = $text;
  $bot_tele1 = str_replace('10 ' , '' , $bot_tele1 );
bot("sendmessage",[
"chat_id"=>$chat_id,
"text"=> "تم الحفظ",
reply_to_message_id =>$message->message_id,
]);
file_put_contents("bot_tele1.txt", $bot_tele1 );
}}

if ( $homsi == "creator" or $homsi == "administrator" ){
if ($message and $member <= $bot_tele1){
bot("sendmessage",[
"chat_id"=>$chat_id,
"text"=> "عذرا لا يمكنني حماية هذا المجموعة
لأن عدد أعضائها أقل من $bot_tele1
عدد أعضاء المجموعة الحالي: $member
",
]);
bot( 'leaveChat' ,[
 'chat_id' =>$chat_id
]);
}}


/*
CH① : @php88
CH② :TALKMANY
توجيه      @php88