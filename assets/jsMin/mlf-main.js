var _____WB$wombat$assign$function_____ = function(name) {return (self._wb_wombat && self._wb_wombat.local_init && self._wb_wombat.local_init(name)) || self[name]; };
if (!self.__WB_pmw) { self.__WB_pmw = function(obj) { this.__WB_source = obj; return this; } }
{
  let window = _____WB$wombat$assign$function_____("window");
  let self = _____WB$wombat$assign$function_____("self");
  let document = _____WB$wombat$assign$function_____("document");
  let location = _____WB$wombat$assign$function_____("location");
  let top = _____WB$wombat$assign$function_____("top");
  let parent = _____WB$wombat$assign$function_____("parent");
  let frames = _____WB$wombat$assign$function_____("frames");
  let opener = _____WB$wombat$assign$function_____("opener");

var currLayer="";function swapImage(b,a){$(b).src=a}function requestPass(){var a="user="+document.requestPwForm.nickmail.value;new Ajax.Updater("responseText","/?action=externalSendPsw",{method:"post",asynchronous:true,parameters:a})}function chageVote(a){if(a=="plus"&&document.votingform.vote.value<4){document.votingform.vote.value++}else{if(a=="minus"&&document.votingform.vote.value>1){document.votingform.vote.value--}}$(responseText).innerHTML="";$(voteImage).src="img/garden/level_"+document.votingform.vote.value+".png"}function sendVoting(){var b=parseInt(document.votingform.vote.value);if(b>0&&b<5){var a="vote="+b+"&uid="+document.votingform.uid.value;new Ajax.Updater("responseText","/?action=externalGardenVote",{method:"post",asynchronous:true,parameters:a})}return false}var selectLang=false;function showLanguageLayer(){if(!selectLang){$("selectLangBox").setStyle({visibility:"visible"});selectLang=true}else{$("selectLangBox").setStyle({visibility:"hidden"});selectLang=false}}function hideLanguageLayer(){$("selectLangBox").setStyle({visibility:"hidden"})}function setLanguageSelected(){$("selectLangBox").setStyle({visibility:"hidden"})}var gtcount=5;var gtcurrent=1;function prevGamesTourimage(a){if(gtcurrent>1){gtcurrent--;$("gamestourimage").src="/img/"+a+"/gamestour/spieltour_"+gtcurrent+".png"}}function nextGamesTourimage(a){if(gtcurrent<gtcount){gtcurrent++;$("gamestourimage").src="/img/"+a+"/gamestour/spieltour_"+gtcurrent+".png"}};

}
/*
     FILE ARCHIVED ON 11:18:54 Jan 05, 2021 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 15:01:50 Dec 15, 2024.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  captures_list: 1.926
  exclusion.robots: 0.039
  exclusion.robots.policy: 0.024
  esindex: 0.017
  cdx.remote: 6.403
  LoadShardBlock: 86.345 (3)
  PetaboxLoader3.datanode: 72.204 (4)
  PetaboxLoader3.resolve: 89.902 (2)
  load_resource: 79.432
*/