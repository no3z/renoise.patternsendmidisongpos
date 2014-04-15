prev_pos = 0
t = 0
device_name = ""


local outputs = renoise.Midi.available_output_devices()
if not table.is_empty(outputs) then 
  device_name = outputs[1]  
  midi_device = renoise.Midi.create_output_device(device_name)   
  midi_device:send {0x90, 0x10, 0x7F}  
  midi_device:send {0xF0, 0x7F, 0x00, 0x06, 0x02, 0xF7}  
end

function stopSend()
  midi_device:close()  
end

function idle_handler()
 t = renoise.song().transport.playback_pos
 if prev_pos ~= t.sequence then  
  midi_device:send {0xF2, t.sequence-1}      
  prev_pos = t.sequence
 end
 
end
 
renoise.tool().app_idle_observable:add_notifier(idle_handler)

  

