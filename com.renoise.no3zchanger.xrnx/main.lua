--Initialize midi output to the first device

local outputs = renoise.Midi.available_output_devices()
if not table.is_empty(outputs) then 
  local device_name = outputs[1]  
  midi_device = renoise.Midi.create_output_device(device_name)    
end

-- Function to call in the idle handler
-- Calculate current measure, taking into account pattern 
-- with lenght=64. Send it via SongPos everytime the value changes.

function idle_handler()
 local prev_pos = 0
 local t = renoise.song().transport.playback_pos
 local measure = (((t.sequence-1) * 4) + (t.line/16))+1
 if prev_pos ~= measure then  
  midi_device:send {0xF2, measure}      
  prev_pos = t.sequence
 end
end

-- Register the idle function 

renoise.tool().app_idle_observable:add_notifier(idle_handler)

-- Someone, somewhere should call this. 

function stopSend()
  midi_device:close()  
end

