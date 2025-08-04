/*
 * BSD 2-Clause License
 *
 * Copyright (c) 2023, Vladimír Ulman
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 *    list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
package org.mastodon.mamut;

import static org.mastodon.app.ui.ViewMenuBuilder.item;
import static org.mastodon.app.ui.ViewMenuBuilder.menu;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

import org.mastodon.app.ui.ViewMenuBuilder;
import org.mastodon.mamut.benchmark.BenchmarkScijavaGui;
import org.mastodon.mamut.plugin.MamutPlugin;
import org.scijava.ui.behaviour.io.gui.CommandDescriptionProvider;
import org.scijava.ui.behaviour.io.gui.CommandDescriptions;
import org.mastodon.ui.keymap.KeyConfigContexts;

import org.scijava.AbstractContextual;
import org.scijava.command.CommandService;
import org.scijava.plugin.Plugin;
import org.scijava.ui.behaviour.util.Actions;
import org.scijava.ui.behaviour.util.AbstractNamedAction;
import org.scijava.ui.behaviour.util.RunnableAction;

@Plugin( type = MamutPlugin.class )
public class BenchmarkPluginFacade extends AbstractContextual implements MamutPlugin
{
	//"IDs" of all plug-ins wrapped in this class
	private static final String EXP_BENCHMARK = "[vexp] benchmark";

	private static final String[] EXP_BENCHMARK_KEYS = { "not mapped" };
	//------------------------------------------------------------------------

	/** titles of this plug-in's menu items */
	private static final Map< String, String > menuTexts = new HashMap<>();
	static
	{
		menuTexts.put( EXP_BENCHMARK, "Benchmark" );
	}
	@Override
	public Map< String, String > getMenuTexts() { return menuTexts; }

	@Override
	public List< ViewMenuBuilder.MenuItem > getMenuItems()
	{
		return Collections.singletonList(
			menu( "Plugins",
				item( EXP_BENCHMARK )
			)
		);
	}

	/** Command descriptions for all provided commands */
	@Plugin( type = Descriptions.class )
	public static class Descriptions extends CommandDescriptionProvider
	{
		public Descriptions()
		{
			super( KeyConfigScopes.MAMUT, KeyConfigContexts.TRACKSCHEME, KeyConfigContexts.BIGDATAVIEWER );
		}

		@Override
		public void getCommandDescriptions( final CommandDescriptions descriptions )
		{
			descriptions.add(EXP_BENCHMARK, EXP_BENCHMARK_KEYS, "Runs suite of tests to benchmark the Mastodon data rendering/visualization pipelines.");
		}
	}
	//------------------------------------------------------------------------


	private final AbstractNamedAction actionBenchmark;

	/** reference to the currently available project in Mastodon */
	private ProjectModel pluginAppModel;

	/** default c'tor: creates Actions available from this plug-in */
	public BenchmarkPluginFacade()
	{
		actionBenchmark = new RunnableAction(EXP_BENCHMARK, this::benchmark);
		updateEnabledActions();
	}

	/** register the actions to the application (with no shortcut keys) */
	@Override
	public void installGlobalActions( final Actions actions )
	{
		actions.namedAction(actionBenchmark, EXP_BENCHMARK_KEYS);
	}

	/** learn about the current project's params */
	@Override
	public void setAppPluginModel( final ProjectModel model )
	{
		//the application reports back to us if some project is available
		this.pluginAppModel = model;
		updateEnabledActions();
	}

	/** enables/disables menu items based on the availability of some project */
	private void updateEnabledActions()
	{
		actionBenchmark.setEnabled( pluginAppModel != null );
	}
	//------------------------------------------------------------------------
	//------------------------------------------------------------------------

	private void benchmark() {
		this.getContext().getService(CommandService.class).run(
			BenchmarkScijavaGui.class, true,
			"mastodonProjectPath", "just don't show this item",
			"projectModel", pluginAppModel
		);
	}
}
